# -*- coding: utf-8 -*-

import asyncio
import websockets

async def connect_to_server():
    uri = "ws://192.168.43.250:3000"
    async with websockets.connect(uri) as websocket:
        # Nh?n tin nh?n ch�o m?ng t? server
        welcome_message = await websocket.recv()
        print(f"< {welcome_message}")

        # G?i tin nh?n d?n server
        await websocket.send("Hello, Server!")
        print("> Hello, Server!")

        # Nh?n ph?n h?i t? server
        response_message = await websocket.recv()
        print(f"< {response_message}")

        # Th�m v�ng l?p d? ti?p t?c nh?n v� g?i tin nh?n
        while True:
            
            response_message = await websocket.recv()
            print(f"< {response_message}")

# Ch?y s? ki?n ch�nh
asyncio.get_event_loop().run_until_complete(connect_to_server())
