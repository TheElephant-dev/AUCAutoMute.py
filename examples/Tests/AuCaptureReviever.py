#!/usr/bin/env python

import asyncio
import websockets

async def waitforcapture(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = f"Hello {name}!"
    await websocket.send(greeting)
    print(f"> sent {greeting}")

start_server = websockets.serve(waitforcapture, 'localhost', 42069)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()