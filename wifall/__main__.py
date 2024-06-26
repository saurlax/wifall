from wifall import config
import wifall.collect
from wifall.test import test
import asyncio
import socketio


sio = socketio.AsyncClient()


async def start():
    print(config['server'])
    await sio.connect(config['server'])
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await sio.disconnect()


@sio.event
async def collect(data):
    await sio.emit('status', 'collecting...')
    file = await wifall.collect.collect()
    print('saved to {}'.format(file))
    await sio.emit('status', 'testing: {}'.format(file))
    await sio.emit('status', 'done: {}, result: {}'.format(file, test(file)))


def main():
    asyncio.run(start())


if __name__ == '__main__':
    main()
