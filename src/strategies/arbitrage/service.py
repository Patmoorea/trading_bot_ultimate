import os
import asyncio
from decimal import Decimal
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from ccxt.async_support import gateio, bingx, okx
from connectors.binance import BinanceConnector
from connectors.blofin import BlofinConnector
from utils.logger import get_logger
from .config import PAIRS, SETTINGS, FEES

load_dotenv()

logger = get_logger()

@dataclass
class OpportuniteArbitrage:
    symbole: str
    exchange_achat: str
    exchange_vente: str
    prix_achat: Decimal
    prix_vente: Decimal
    volume: Decimal
    profit: Decimal
    horodatage: float

class GestionnaireExchanges:
    def __init__(self):
        self.exchanges = {
            'binance': BinanceConnector(),
            'gateio': gateio({
                'apiKey': os.getenv('GATEIO_API_KEY'),
                'secret': os.getenv('GATEIO_API_SECRET'),
                'enableRateLimit': True
            }),
            'bingx': bingx({
                'apiKey': os.getenv('BINGX_API_KEY'),
                'secret': os.getenv('BINGX_API_SECRET'),
                'enableRateLimit': True
            }),
            'okx': okx({
                'apiKey': os.getenv('OKX_API_KEY'),
                'secret': os.getenv('OKX_API_SECRET'),
                'password': os.getenv('OKX_PASSPHRASE'),
                'enableRateLimit': True
            }),
            'blofin': BlofinConnector()
        }
    
    async def obtenir_carnet_ordres(self, exchange: str, symbole: str):
        try:
            if exchange == 'blofin':
                return await self.exchanges[exchange].get_order_book(symbole)
            else:
                carnet = await self.exchanges[exchange].fetch_order_book(symbole)
                return Decimal(carnet['bids'][0][0]), Decimal(carnet['asks'][0][0])
        except Exception as e:
            logger.warning(f"Échec récupération carnet d'ordres sur {exchange}: {str(e)}")
            return Decimal(0), Decimal('Infinity')
    
    async def creer_ordre(self, exchange: str, symbole: str, cote: str, montant: Decimal, prix: Decimal = None):
        try:
            if exchange == 'blofin':
                return await self.exchanges[exchange].create_order(symbole, cote, montant, prix)
            else:
                return await self.exchanges[exchange].create_order(symbole, 'market', cote, float(montant))
        except Exception as e:
            logger.error(f"Échec création ordre sur {exchange}: {str(e)}")
            raise

class MoteurArbitrage:
    def __init__(self):
        self.gestionnaire = GestionnaireExchanges()
        self.ordres_actifs = {}
    
    async def scanner_opportunites(self) -> List[OpportuniteArbitrage]:
        opportunites = []
        tâches = []
        
        for symbole in PAIRS:
            for exchange, paire in PAIRS[symbole].items():
                tâches.append(self._obtenir_prix(exchange, paire, symbole))
        
        prix = await asyncio.gather(*tâches)
        
        prix_par_symbole = {}
        for exchange, symbole, bid, ask in prix:
            if symbole not in prix_par_symbole:
                prix_par_symbole[symbole] = {}
            prix_par_symbole[symbole][exchange] = (bid, ask)
        
        for symbole in prix_par_symbole:
            meilleur_bid = {'exchange': None, 'prix': Decimal(0)}
            meilleur_ask = {'exchange': None, 'prix': Decimal('Infinity')}
            
            for exchange in prix_par_symbole[symbole]:
                bid, ask = prix_par_symbole[symbole][exchange]
                
                if bid and ask:
                    bid_ajuste = bid * (1 - FEES[exchange]['taker'] * SETTINGS['fee_adjustment'] - bid * SETTINGS['max_slippage'])
                    ask_ajuste = ask * (1 + FEES[exchange]['taker'] * SETTINGS['fee_adjustment'] + ask * SETTINGS['max_slippage'])
                    
                    if bid_ajuste > meilleur_bid['prix']:
                        meilleur_bid = {'exchange': exchange, 'prix': bid_ajuste}
                    
                    if ask_ajuste < meilleur_ask['prix']:
                        meilleur_ask = {'exchange': exchange, 'prix': ask_ajuste}
            
            if meilleur_bid['exchange'] and meilleur_ask['exchange'] and meilleur_bid['exchange'] != meilleur_ask['exchange']:
                profit = (meilleur_bid['prix'] - meilleur_ask['prix']) / meilleur_ask['prix']
                if profit >= SETTINGS['profit_threshold']:
                    volume = Decimal(SETTINGS['max_order_value']) / meilleur_ask['prix']
                    opportunites.append(
                        OpportuniteArbitrage(
                            symbole=symbole,
                            exchange_achat=meilleur_ask['exchange'],
                            exchange_vente=meilleur_bid['exchange'],
                            prix_achat=meilleur_ask['prix'],
                            prix_vente=meilleur_bid['prix'],
                            volume=volume,
                            profit=profit,
                            horodatage=time.time()
                        )
                    )
        
        return opportunites
    
    async def _obtenir_prix(self, exchange: str, paire: str, symbole: str):
        bid, ask = await self.gestionnaire.obtenir_carnet_ordres(exchange, paire)
        return (exchange, symbole, bid, ask)
    
    async def executer_arbitrage(self, opportunite: OpportuniteArbitrage):
        try:
            # 1. Achat sur l'exchange le moins cher
            paire_achat = PAIRS[opportunite.symbole][opportunite.exchange_achat]
            logger.info(f"Passage ordre d'achat sur {opportunite.exchange_achat} pour {paire_achat}...")
            ordre_achat = await self.gestionnaire.creer_ordre(
                exchange=opportunite.exchange_achat,
                symbole=paire_achat,
                cote='buy',
                montant=opportunite.volume,
                prix=opportunite.prix_achat
            )
            
            # 2. Vente sur l'exchange le plus cher
            paire_vente = PAIRS[opportunite.symbole][opportunite.exchange_vente]
            logger.info(f"Passage ordre de vente sur {opportunite.exchange_vente} pour {paire_vente}...")
            ordre_vente = await self.gestionnaire.creer_ordre(
                exchange=opportunite.exchange_vente,
                symbole=paire_vente,
                cote='sell',
                montant=opportunite.volume,
                prix=opportunite.prix_vente
            )
            
            logger.info(
                f"ARBITRAGE RÉUSSI | {opportunite.symbole} | "
                f"Achat@{opportunite.exchange_achat}: {ordre_achat.get('price', 'N/A')} | "
                f"Vente@{opportunite.exchange_vente}: {ordre_vente.get('price', 'N/A')} | "
                f"Profit estimé: {opportunite.profit:.2%}"
            )
            
            return opportunite.profit
            
        except Exception as e:
            logger.error(f"Échec arbitrage: {str(e)}")
            await self._annuler_ordres(opportunite)
            raise
    
    async def _annuler_ordres(self, opportunite: OpportuniteArbitrage):
        for exchange in [opportunite.exchange_achat, opportunite.exchange_vente]:
            try:
                if exchange != 'blofin':
                    await self.exchanges[exchange].cancel_all_orders(PAIRS[opportunite.symbole][exchange])
            except Exception as e:
                logger.warning(f"Échec annulation ordres sur {exchange}: {str(e)}")
