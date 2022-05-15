import asyncio
import sys

import aiohttp

import api


async def _main(login: str, password: str, town: str) -> None:
    async with aiohttp.ClientSession() as sess:
        print(await api.get_data(sess, login, password, town))


if __name__ == "__main__":
    if not len(sys.argv) == 4:
        print("Usage: python3 api.py user pass town")
        sys.exit(0)
    user_param = sys.argv[1]
    passw_param = sys.argv[2]
    town_param = sys.argv[3]

    asyncio.get_event_loop().run_until_complete(_main(user_param, passw_param, town_param))
