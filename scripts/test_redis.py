import asyncio

from app.services.redis import RedisRepository

repository = RedisRepository()


async def main():
    canal = "699558173654"

    await repository.pause_ia(canal)
    print("Pausado:", await repository.is_paused(canal))

    await repository.resume_ia(canal)
    print("Pausado:", await repository.is_paused(canal))


asyncio.run(main())
