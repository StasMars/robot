import asyncio
import sys

async def robot(start_from=0):
    count = start_from
    while True:
        print(count)
        count += 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    asyncio.run(robot(start_from))
