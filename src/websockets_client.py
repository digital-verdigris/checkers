import argparse
import asyncio
import json
import logging
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

class checkers_websockets_client:
    def __init__(self, role, signaling_url="ws://localhost:5000", game_instance = None, password = None):
        self.role = role
        self.signaling_url = signaling_url
        self.pc = RTCPeerConnection()
        self.channel = None
        self.game_instance = game_instance  # Reference to the game
        self.loop = None  # Will store the event loop running this client
        self.password = password
        self.secret_key = self.derive_key(password) if password else None  # Generate AES key if password is provided
    
    def derive_key(self, password):
        """Derives a 32-byte AES key from the password using PBKDF2."""
        salt = b"checkers_salt"  # Fixed salt (MUST be the same for both players)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 requires a 32-byte key
            salt=salt,
            iterations=100000,  # High iterations for security
            backend=default_backend()
        )
        return kdf.derive(password.encode())  # Convert password into a secure encryption key
    def encrypt_message(self, plaintext):
        """Encrypts a message using AES-GCM."""
        if not self.secret_key:
            return plaintext  # If no encryption key is set, send plaintext

        iv = os.urandom(12)  # Generate a unique IV for each message
        cipher = Cipher(algorithms.AES(self.secret_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(iv + encryptor.tag + ciphertext).decode()  # Base64 encode for transmission

    def decrypt_message(self, encrypted_message):
        """Decrypts a message using AES-GCM."""
        if not self.secret_key:
            return encrypted_message  # If no key is set, assume plaintext

        try:
            data = base64.b64decode(encrypted_message)
            iv, tag, ciphertext = data[:12], data[12:28], data[28:]
            cipher = Cipher(algorithms.AES(self.secret_key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

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
        """Encrypts and sends a move over WebRTC."""
        if self.channel and self.channel.readyState == "open":
            move_json = json.dumps({"type": "move", "data": move})  # Convert move to JSON
            encrypted_move = self.encrypt_message(move_json)  # Encrypt JSON message
            print(f"Sending encrypted move: {encrypted_move}")
            if self.loop:
                self.loop.call_soon_threadsafe(lambda: self.channel.send(encrypted_move))
            else:
                print("Client loop not available!")
        else:
            print("Data channel not open yet.")


    def on_message(self, message):
        """Handles incoming encrypted messages. Decrypts and processes move data."""
        print(f"Received encrypted: {message}")
        decrypted_message = self.decrypt_message(message)  # Decrypt message
        if decrypted_message:
            try:
                data = json.loads(decrypted_message.decode())  # Convert back to JSON
                if data.get("type") == "move":
                    move = data["data"]
                    print(f"Decrypted move: {move}")
                    if self.game_instance:
                        self.game_instance.receive_move(move)
                else:
                    print("Received non-move message.")
            except json.JSONDecodeError:
                print("Invalid JSON format")
        else:
            print("Failed to decrypt message.")


    def on_open(self):
        print("Data channel is open!")
        if self.game_instance:
            self.game_instance.notify_data_channel_opened()
        # Remove terminal input for integrated game usage.
        # asyncio.create_task(self.terminal_input(self.channel))

    def on_datachannel(self, channel):
        self.channel = channel
        print(f"Data channel received: {channel.label}")
        channel.on("message", self.on_message)
        if self.game_instance:
            self.game_instance.notify_data_channel_opened()

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
