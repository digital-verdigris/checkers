import argparse
import asyncio
import json
import logging
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription

class checkers_websockets_client:
    def __init__(self, role, signaling_url="ws://localhost:5000"):
        self.role = role
        self.signaling_url = signaling_url
        self.pc = RTCPeerConnection()
        self.channel = None

    async def connect_signaling(self):
        async with websockets.connect(self.signaling_url) as signaling:
            print(f"Connected to signaling server as {self.role}")
            await self.run(signaling)
            await asyncio.Future()  # Keep the connection alive

    async def run(self, signaling):
        if self.role == "offer":
            self.channel = self.pc.createDataChannel("chat")
            self.channel.on("open", self.on_open)
            self.channel.on("message", self.on_message)
            offer = await self.pc.createOffer()
            await self.pc.setLocalDescription(offer)
            await signaling.send(json.dumps({"sdp": self.pc.localDescription.sdp, "type": self.pc.localDescription.type}))
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
                    await signaling.send(json.dumps({"sdp": self.pc.localDescription.sdp, "type": self.pc.localDescription.type}))
    
    def on_open(self):
        print("Data channel is open!")
        if self.role == "offer":
            self.channel.send("Hello from offerer!")
        asyncio.create_task(self.terminal_input(self.channel))
    
    def on_datachannel(self, channel):
        self.channel = channel
        print(f"Data channel received: {channel.label}")
        channel.on("message", self.on_message)
        if channel.readyState == "open":
            asyncio.create_task(self.delayed_send(channel))
            asyncio.create_task(self.terminal_input(channel))
    
    async def delayed_send(self, channel):
        while channel.readyState != "open":
            await asyncio.sleep(0.1)
        await asyncio.sleep(0.1)
        channel.send("Hello from answerer!")
    
    async def terminal_input(self, channel):
        loop = asyncio.get_running_loop()
        while True:
            message = await loop.run_in_executor(None, input, "Enter message: ")
            if channel.readyState == "open":
                channel.send(message)
            else:
                print("Data channel not open yet.")
    
    def on_message(self, message):
        print(f"Received: {message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC signaling client")
    parser.add_argument("role", choices=["offer", "answer"], help="Role: offer or answer")
    args = parser.parse_args()
    client = checkers_websockets_client(args.role)
    asyncio.run(client.connect_signaling())
