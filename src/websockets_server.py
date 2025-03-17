import asyncio
import websockets
import logging
import ssl
import time

#logging.basicConfig(level=logging.DEBUG)

class checkers_websockets_server:
    def __init__(self, host="localhost", port=5000, cert="cert.pem", key="cert.key", rate_limit=5, per_seconds=1):
        self.host = host
        self.port = port
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain(certfile=cert, keyfile=key)
        self.connected = set()
        self.message_counts = {} 
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds

    async def handler(self, websocket):
        self.connected.add(websocket)
        self.message_counts[websocket] = []
        logging.debug(f"New client connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                if not self.is_rate_limited(websocket):
                    sanitized_message = self.sanitize_message(message)
                    logging.debug(f"Received message from {websocket.remote_address}: {message}")
                    await self.broadcast(message, websocket)
                else:
                    logging.warning(f"Rate limit exceeded: {websocket.remote_address}")
        except websockets.exceptions.ConnectionClosed as e:
            logging.debug(f"Client {websocket.remote_address} disconnected: {e}")
        finally:
            self.connected.remove(websocket)
            logging.debug(f"Removed connection: {websocket.remote_address}")

    def is_rate_limited(self, websocket):
        """Returns True if client exceeded rate limit."""
        now = time.time()
        timestamps = self.message_counts[websocket]

        self.message_counts[websocket] = [t for t in timestamps if now - t < self.per_seconds]

        self.message_counts[websocket].append(now)
        return len(self.message_counts[websocket]) > self.rate_limit

    def sanitize_message(self, message):
        """Basic message sanitization (strip, limit length)."""
        sanitized = message.strip()[:256]  # Trim message to 256 characters
        return sanitized
    
    async def broadcast(self, message, sender):
        for conn in self.connected:
            if conn != sender:
                logging.debug(f"Forwarding message to {conn.remote_address}")
                await conn.send(message)

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port, ssl=self.ssl_context):
            logging.info(f"Signaling server is running on wss://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = checkers_websockets_server()
    asyncio.run(server.start())
