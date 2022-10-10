#!/usr/bin/env python

import asyncio
import websockets

x=0
async def hello():
    global x
    while True:
        async with websockets.connect('ws://localhost:42069/api') as websocket:
            x+=1
            # x = input('what data would you like to send?')
            await websocket.send(f'{x}')
            print(f'   - Sending "{x}"')


            response = await websocket.recv()
            print(f'bot responded with: "{response}"')

asyncio.get_event_loop().run_until_complete(hello())
