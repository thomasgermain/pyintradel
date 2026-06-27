import asyncio
import json
import sys

import aiohttp

from pyintradel import api


async def _run(login: str, password: str, town: str) -> None:
    async with aiohttp.ClientSession() as sess:
        json.dump(await api.get_data(sess, login, password, town), sys.stdout, indent=2)


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: pyintradel user pass town")
        sys.exit(0)

    asyncio.run(_run(sys.argv[1], sys.argv[2], sys.argv[3]))


if __name__ == "__main__":
    main()
