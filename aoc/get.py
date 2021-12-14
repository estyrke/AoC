from logging import StreamHandler
import os
from typing import cast
import requests
from urllib.parse import urljoin
import sys
from . import logging
from datetime import datetime
import time
import re

from aoc.util import base_url, convert_tag_to_md, session_cookie


logger = logging.getLogger(__name__)


def main():
    year = int(sys.argv[1])
    day = int(sys.argv[2])

    logging.init_logging()

    get(year, day)


def get(year: int, day: int):
    description_url = urljoin(base_url(), f"{year}/day/{day}")
    input_url = urljoin(description_url, f"{day}/input")

    basedir = os.path.dirname(__file__)
    input_filename = f"{basedir}/{year}/{day}_input.txt"
    part1_py_filename = f"{basedir}/{year}/{day}_1.py"
    part2_py_filename = f"{basedir}/{year}/{day}_2.py"

    # Wait for puzzle start
    puzzle_start = datetime.fromisoformat(
        f"{year}-12-{day:02}T05:00:01+00:00"
    ).astimezone()
    try:
        while datetime.now().astimezone() < puzzle_start:
            time_left = puzzle_start - datetime.now().astimezone()
            cast(StreamHandler, logger.root.handlers[0]).terminator = "\r"
            logger.info(f"Not availablel yet. Will try again in {time_left}")
            cast(StreamHandler, logger.root.handlers[0]).terminator = "\n"

            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        logger.info("")

    s = requests.session()
    s.cookies.set("session", session_cookie())

    if not os.path.exists(input_filename):
        logger.info("Getting input from %s", input_url)

        with s.get(input_url) as u:
            if u.text.startswith("Please don't"):
                logger.error("Puzzle not available yet!")
                return
            with open(input_filename, "w") as input_txt:
                input_txt.write(u.text)

    logger.info("Getting description from %s", description_url)

    with s.get(description_url) as u:
        html = u.text

    desc = convert_tag_to_md(html, "article")
    desc2 = convert_tag_to_md(html, "article", 2)

    if desc is None:
        raise RuntimeError(f"Unable to find the first part description!")

    if not os.path.exists(part1_py_filename):
        logger.info(f"Generating code scaffold for day {day}, part 1")
        part1_code = make_scaffold(year, day, 1, desc)
        with open(part1_py_filename, "w") as part1_py:
            part1_py.write(part1_code)

    if desc2:
        if not os.path.exists(part2_py_filename):
            logger.info(f"Generating code scaffold for day {day}, part 2")
            part2_code = make_scaffold(year, day, 2, desc2)
            with open(part2_py_filename, "w") as part2_py:
                part2_py.write(part2_code)
    else:
        logger.info("There is no part 2 in the document yet - solve part 1 first")


def make_scaffold(year: int, day: int, level: int, desc: str) -> str:
    desc = "\n".join([f"# {l}" for l in desc.splitlines()])
    basedir = os.path.dirname(__file__)

    if level == 2:
        # Get existing part 1 code
        code = get_part1_code(f"{basedir}/{year}/{day}_1.py", desc)
    else:
        with open(f"{basedir}/solution_template.py") as tmpl:
            code = tmpl.read().format(desc=desc)

    return code


def get_part1_code(part1_filename: str, desc: str):
    with open(part1_filename) as part1_py:
        code = part1_py.read()

    code = code.replace("{", "{{").replace("}", "}}")
    return (
        re.sub("(?<=###\n).*(?=\n###)", "{desc}", code, 1, re.MULTILINE | re.DOTALL)
        .format(desc=desc)
        .replace("{{", "{")
        .replace("}}", "}")
    )


if __name__ == "__main__":
    main()
