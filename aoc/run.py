import logging
import os
import sys
import importlib
from urllib.parse import urljoin

import requests

from aoc.util import base_url, convert_tag_to_md, session_cookie
from aoc.get import get


logger = logging.getLogger(__name__)


def run(year: int, day: int, part: int, test=False):

    logging.basicConfig(level=logging.INFO)

    mod = importlib.import_module(f"aoc.{year}.{day}_{part}")

    basedir = os.path.dirname(__file__)
    with open(f"{basedir}/{year}/{day}_input.txt") as inp:
        answer = mod.solve(inp)

    if answer is not None:
        answer_url = urljoin(base_url(), f"{year}/day/{day}/answer")

        if test:
            print(f"NOT posting answer {answer} to {answer_url}")
            return

        s = requests.session()
        s.cookies.set("session", session_cookie())
        print(f"Posting answer {answer} to {answer_url}")
        with s.post(answer_url, data={"level": part, "answer": answer}) as u:
            print(convert_tag_to_md(u.text, "article"))
            if part == 1 and "That's the right answer" in u.text:
                # Download part 2
                get(year, day)


def main():
    year = int(sys.argv[1])
    day = int(sys.argv[2])
    part = int(sys.argv[3])
    test = len(sys.argv) >= 5 and sys.argv[4] == "test"
    run(year, day, part, test)


if __name__ == "__main__":
    main()
