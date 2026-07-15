import argparse
import asyncio
import json
import sys

import aiohttp

from pyintradel import api


async def _run(
    login: str | None, password: str | None, town: str | None, cookie: str | None
) -> None:
    async with aiohttp.ClientSession() as sess:
        data = await api.get_data(sess, login, password, town, cookie=cookie)
        json.dump(data, sys.stdout, indent=2)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pyintradel",
        description="Usage: pyintradel user pass town OR pyintradel --cookie COOKIE",
    )
    parser.add_argument("login", nargs="?", help="Login")
    parser.add_argument("password", nargs="?", help="Password")
    parser.add_argument("town", nargs="?", help="Town, see pyintradel/api/towns.py")
    parser.add_argument(
        "--cookie",
        help="Session cookie captured from an already logged-in browser, "
        "used instead of login/password/town",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args(sys.argv[1:])

    if not args.cookie and not (args.login and args.password and args.town):
        print("Usage: pyintradel user pass town OR pyintradel --cookie COOKIE")
        sys.exit(1)

    asyncio.run(_run(args.login, args.password, args.town, args.cookie))


if __name__ == "__main__":
    main()
