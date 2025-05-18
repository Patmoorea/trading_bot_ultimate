from typing import List, Dict
from decimal import Decimal
import asyncio
import logging
import time
from ....exchanges.base_exchange import BaseExchange

class ArbitrageScanner:
    def __init__(self, exchanges: List[BaseExchange], min_profit_threshold: Decimal = Decimal('0.001')):
        if min_profit_threshold <= Decimal('0'):
            raise ValueError("Le seuil de profit minimum doit être positif")
            
        self.exchanges = exchanges
        self.min_profit_threshold = min_profit_threshold
        self.logger = logging.getLogger(__name__)

    async def scan_opportunities(self, symbol: str, *, trade_amount: Decimal = Decimal('1.0')) -> List[Dict]:
        start_time = time.perf_counter()
        opportunities = []
        
        try:
            if not self.exchanges:
                self.logger.debug("Liste d'exchanges vide")
                return opportunities

            self.logger.debug(f"Début scan pour {symbol} sur {len(self.exchanges)} exchanges")
            
            # Récupération des order books
            order_books = await asyncio.gather(
                *[self._get_order_book(exchange, symbol) for exchange in self.exchanges],
                return_exceptions=True
            )

            valid_order_books = []
            valid_exchanges = []

            for i, result in enumerate(order_books):
                if isinstance(result, Exception):
                    self.logger.error(f"Erreur pour {self.exchanges[i].__class__.__name__}: {str(result)}")
                    continue
                if not result.get('asks') or not result.get('bids'):
                    self.logger.warning(f"Order book vide pour {self.exchanges[i].__class__.__name__}")
                    continue
                valid_order_books.append(result)
                valid_exchanges.append(self.exchanges[i])

            for i, buy_exchange in enumerate(valid_exchanges):
                buy_book = valid_order_books[i]
                
                if not buy_book['asks'] or buy_book['asks'][0][1] < trade_amount:
                    continue

                for j, sell_exchange in enumerate(valid_exchanges):
                    if i == j:
                        continue
                        
                    sell_book = valid_order_books[j]
                    if not sell_book['bids'] or sell_book['bids'][0][1] < trade_amount:
                        continue

                    buy_price = buy_book['asks'][0][0]
                    sell_price = sell_book['bids'][0][0]
                    
                    # Calcul du profit brut et net (pour l'instant sans frais)
                    gross_profit = (sell_price - buy_price) * trade_amount
                    total_fees = Decimal('0')  # À implémenter avec le calculateur de frais
                    net_profit = gross_profit - total_fees
                    profit_ratio = net_profit / (buy_price * trade_amount)

                    if profit_ratio > self.min_profit_threshold:
                        opportunities.append({
                            'buy_exchange': buy_exchange.__class__.__name__,
                            'sell_exchange': sell_exchange.__class__.__name__,
                            'symbol': symbol,
                            'amount': trade_amount,
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'gross_profit': gross_profit,
                            'total_fees': total_fees,
                            'net_profit': net_profit,
                            'profit_ratio': profit_ratio
                        })

            opportunities.sort(key=lambda x: x['net_profit'], reverse=True)

        except Exception as e:
            self.logger.error(f"Erreur scan_opportunities: {str(e)}")
        finally:
            elapsed = time.perf_counter() - start_time
            self.logger.debug(
                f"Scan completed in {elapsed:.3f}s - "
                f"Found {len(opportunities)} opportunities for {symbol}"
            )
            
        return opportunities

    async def _get_order_book(self, exchange: BaseExchange, symbol: str) -> Dict:
        try:
            return exchange.get_order_book(symbol)
        except Exception as e:
            self.logger.error(f"Erreur get_order_book pour {exchange.__class__.__name__}: {str(e)}")
            return {'asks': [[Decimal('inf'), Decimal('0')]], 'bids': [[Decimal('0'), Decimal('0')]]}

    def get_current_utc(self) -> str:
        """Retourne le timestamp UTC au format YYYY-MM-DD HH:MM:SS"""
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    def get_user(self) -> str:
        """Retourne l'utilisateur courant"""
        # Pour les tests et la reproductibilité, on peut forcer un utilisateur avec TRADING_BOT_USER
        return os.environ.get('TRADING_BOT_USER', os.environ.get('USER', 'unknown'))

    async def execute_arbitrage(self, opportunity: Dict) -> Dict:
        """Exécute une opportunité d'arbitrage"""
        execution_time = self.get_current_utc()
        execution_user = self.get_user()
        
        try:
            # Validation des données
            required_fields = ['buy_exchange', 'sell_exchange', 'symbol', 'amount', 
                             'buy_price', 'sell_price']
            if not all(field in opportunity for field in required_fields):
                raise ValueError("Opportunité invalide - champs manquants")

            # Logs d'exécution
            self.logger.info(f"[{execution_time}] Utilisateur {execution_user} - "
                           f"Exécution arbitrage {opportunity['symbol']} : "
                           f"achat sur {opportunity['buy_exchange']} @ {opportunity['buy_price']}, "
                           f"vente sur {opportunity['sell_exchange']} @ {opportunity['sell_price']}")

            # TODO: Implémenter l'exécution réelle des ordres
            # Pour l'instant on retourne juste les détails de l'exécution
            return {
                'execution_time': execution_time,
                'execution_user': execution_user,
                'status': 'simulated',
                'details': opportunity
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de l'arbitrage: {str(e)}")
            return {
                'execution_time': execution_time,
                'execution_user': execution_user,
                'status': 'error',
                'error': str(e)
            }
