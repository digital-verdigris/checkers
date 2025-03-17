# Verdigris Checkers

## Description
This a P2P and LAN checkers application that focuses on providing proper P2P security to connect players using WebRTC and Secure WebSockets

## Running The Project
Running the project require a couple steps
1. Start the signaling server (if using P2P)
    This is accomplished by calling 'python3 src/websockets_server.py' in the root folder this must be done seperately from running the main application

2. Starting the main application
    This is accomplished by calling 'python3 src/main.py' in the root folder.
    From here you can input 1 in the terminal to start the LAN version of the application or 2 to start the P2P version of the application
```sh
