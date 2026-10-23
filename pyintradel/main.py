import argparse
import asyncio
import json
import sys

import aiohttp

from pyintradel import api


async def _run(cookie: str) -> None:
    async with aiohttp.ClientSession() as sess:
        data = await api.get_data(sess, cookie)
        json.dump(data, sys.stdout, indent=2)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="pyintradel")
    parser.add_argument(
        "--cookie",
        required=True,
        help="Session cookie captured from an already logged-in browser",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args(sys.argv[1:])
    asyncio.run(_run(args.cookie))


if __name__ == "__main__":
    main()
