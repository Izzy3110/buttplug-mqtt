import asyncio

import socketio


async def main():
    # asyncio
    async with socketio.AsyncSimpleClient() as sio:
        await sio.connect(url="http://127.0.0.1:5005/")
        await sio.emit(event="external_set", data={"value": 40})

if __name__ == '__main__':
    asyncio.run(main())
