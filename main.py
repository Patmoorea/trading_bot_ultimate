#!/usr/bin/env python3
import asyncio
import logging
from modules.arbitrage_engine import ArbitrageEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def safe_arbitrage():
    engine = ArbitrageEngine()
    while True:
        try:
            opportunities = await asyncio.wait_for(
                engine.check_opportunities_v2(),
                timeout=60
            )
            if opportunities:
                logger.info(f"Opportunités trouvées: {len(opportunities)}")
            await asyncio.sleep(30)
        except asyncio.TimeoutError:
            logger.warning("Timeout - Redémarrage du cycle")
        except Exception as e:
            logger.error(f"Erreur critique: {str(e)}", exc_info=True)
            await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(safe_arbitrage())
    except KeyboardInterrupt:
        print("Arrêt propre du bot")
