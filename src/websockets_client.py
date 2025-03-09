import argparse
import asyncio
import json
import logging
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription

class checkers_websockets_client:
    def __init__(self, role, signaling_url="ws://localhost:5000", game_instance=None):
        self.role = role
        self.signaling_url = signaling_url
        self.pc = RTCPeerConnection()
        self.channel = None
        self.game_instance = game_instance  # Reference to the game
        self.loop = None  # Will store the event loop running this client

    async def connect_signaling(self):
        async with websockets.connect(self.signaling_url) as signaling:
            print(f"Connected to signaling server as {self.role}")
            self.loop = asyncio.get_running_loop()  # Save the current event loop
            await self.run(signaling)
            await self.keep_alive()

    async def run(self, signaling):
        if self.role == "offer":
            self.channel = self.pc.createDataChannel("chat")
            self.channel.on("open", self.on_open)
            self.channel.on("message", self.on_message)
            offer = await self.pc.createOffer()
            await self.pc.setLocalDescription(offer)
            await signaling.send(json.dumps({
                "sdp": self.pc.localDescription.sdp, 
                "type": self.pc.localDescription.type
            }))
        else:
            self.pc.on("datachannel", self.on_datachannel)
        
        async for message in signaling:
            data = json.loads(message)
            if "sdp" in data and "type" in data:
                desc = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await self.pc.setRemoteDescription(desc)
                if desc.type == "offer":
                    answer = await self.pc.createAnswer()
                    await self.pc.setLocalDescription(answer)
                    await signaling.send(json.dumps({
                        "sdp": self.pc.localDescription.sdp, 
                        "type": self.pc.localDescription.type
                    }))

    async def keep_alive(self):
        # Simple keep-alive loop to ensure the event loop stays active.
        while True:
            await asyncio.sleep(0.1)

    def send_move(self, move):
        """Schedules sending a move (e.g., a tuple representing the move) as a JSON message on the client's event loop."""
        if self.channel and self.channel.readyState == "open":
            message = json.dumps({"type": "move", "data": move})
            print(f"Sending move: {message}")
            # Schedule the send on the client’s own event loop
            if self.loop:
                self.loop.call_soon_threadsafe(lambda: self.channel.send(message))
            else:
                print("Client loop not available!")
        else:
            print("Data channel not open yet.")

    def on_message(self, message):
        """Handles incoming messages. If the message is a move, pass it to the game instance."""
        print(f"Received: {message}")
        try:
            data = json.loads(message)
            if data.get("type") == "move":
                move = data["data"]
                print(f"Received move: {move}")
                if self.game_instance:
                    self.game_instance.receive_move(move)
            else:
                print("Received non-move message.")
        except json.JSONDecodeError:
            print("Invalid message format")

    def on_open(self):
        print("Data channel is open!")
        # Remove terminal input for integrated game usage.
        # asyncio.create_task(self.terminal_input(self.channel))

    def on_datachannel(self, channel):
        self.channel = channel
        print(f"Data channel received: {channel.label}")
        channel.on("message", self.on_message)
        # Terminal input disabled for integration.
        # if channel.readyState == "open":
        #     asyncio.create_task(self.delayed_send(channel))
        #     asyncio.create_task(self.terminal_input(channel))
    
    async def delayed_send(self, channel):
        while channel.readyState != "open":
            await asyncio.sleep(0.1)
        await asyncio.sleep(0.1)
    
    async def terminal_input(self, channel):
        """Terminal input loop for testing. Not used in integrated game mode."""
        loop = asyncio.get_running_loop()
        while True:
            message = await loop.run_in_executor(None, input, "Enter message: ")
            if channel.readyState == "open":
                channel.send(message)
            else:
                print("Data channel not open yet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC signaling client")
    parser.add_argument("role", choices=["offer", "answer"], help="Role: offer or answer")
    args = parser.parse_args()
    client = checkers_websockets_client(args.role)
    asyncio.run(client.connect_signaling())
