import asyncio
import websockets
import logging

#logging.basicConfig(level=logging.DEBUG)

class checkers_websockets_server:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.connected = set()

    async def handler(self, websocket):
        self.connected.add(websocket)
        logging.debug(f"New client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                logging.debug(f"Received message from {websocket.remote_address}: {message}")
                await self.broadcast(message, websocket)
        except websockets.exceptions.ConnectionClosed as e:
            logging.debug(f"Client {websocket.remote_address} disconnected: {e}")
        finally:
            self.connected.remove(websocket)
            logging.debug(f"Removed connection: {websocket.remote_address}")

    async def broadcast(self, message, sender):
        for conn in self.connected:
            if conn != sender:
                logging.debug(f"Forwarding message to {conn.remote_address}")
                await conn.send(message)

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            logging.info(f"Signaling server is running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = checkers_websockets_server()
    asyncio.run(server.start())
