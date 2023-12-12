from logging import StreamHandler
import os
from typing import cast
from urllib.parse import urljoin
import sys
from . import log
from datetime import datetime
import time

from aoc.util import base_url, create_session


logger = log.getLogger(__name__)


def main():
    year = int(sys.argv[1])
    day = int(sys.argv[2])

    log.init_logging()

    get(year, day)


def get(year: int, day: int):
    input_url = urljoin(base_url(), f"{year}/day/{day}/input")

    basedir = os.path.dirname(__file__)
    input_filename = f"{basedir}/{year}/{day}_input.txt"
    solution_py_filename = f"{basedir}/{year}/{day}.py"

    # Wait for puzzle start
    puzzle_start = datetime.fromisoformat(
        f"{year}-12-{day:02}T05:00:01+00:00"
    ).astimezone()
    try:
        while datetime.now().astimezone() < puzzle_start:
            time_left = puzzle_start - datetime.now().astimezone()
            cast(StreamHandler, logger.root.handlers[0]).terminator = "\r"
            logger.info(f"Not available yet. Will try again in {time_left}")
            cast(StreamHandler, logger.root.handlers[0]).terminator = "\n"

            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        logger.info("")

    s = create_session()

    if not os.path.exists(input_filename):
        logger.info("Getting input from %s", input_url)

        with s.get(input_url) as u:
            if u.text.startswith("Please don't"):
                logger.error("Puzzle not available yet!")
                return
            with open(input_filename, "w") as input_txt:
                input_txt.write(u.text)

    if not os.path.exists(solution_py_filename):
        logger.info(f"Generating code scaffold for day {day}")
        code = make_scaffold()
        with open(solution_py_filename, "w") as solution_py:
            solution_py.write(code)


def make_scaffold() -> str:
    basedir = os.path.dirname(__file__)

    with open(f"{basedir}/templates/solution_template.py") as tmpl:
        code = tmpl.read()

    return code


if __name__ == "__main__":
    main()
