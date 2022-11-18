import asyncio


async def a():
    print(" a")
    await asyncio.sleep(0)
    print("resuming a")


async def b():
    print("in b")


async def main():
    await asyncio.gather(a(), b())


if __name__ == "__main__":
    asyncio.run(main())
