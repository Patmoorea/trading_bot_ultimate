import lz4.frame
import websockets
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import deque

class OptimizedWSClient:
    def __init__(self, max_streams=12, buffer_size=1000):
        self.compression_level = lz4.frame.COMPRESSIONLEVEL_MAX
        self.buffers = [deque(maxlen=buffer_size) for _ in range(max_streams)]
        self.connections = {}
        
    async def connect(self, urls):
        with ThreadPoolExecutor(max_workers=12) as executor:
            tasks = [
                asyncio.create_task(self._manage_stream(i, url, executor))
                for i, url in enumerate(urls[:12])
            ]
            await asyncio.gather(*tasks)
    
    async def _manage_stream(self, stream_id, url, executor):
        async with websockets.connect(url) as ws:
            self.connections[stream_id] = ws
            while True:
                raw = await ws.recv()
                if isinstance(raw, str):
                    raw = raw.encode('utf-8')
                compressed = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    self._compress_data,
                    raw
                )
                self.buffers[stream_id].append(compressed)
    
    def _compress_data(self, data):
        return lz4.frame.compress(
            data,
            compression_level=self.compression_level,
            store_size=False
        )
