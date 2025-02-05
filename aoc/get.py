from logging import StreamHandler
from pathlib import Path
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
    day_url = urljoin(base_url(), f"{year}/day/{day}")
    input_url = urljoin(base_url(), f"{year}/day/{day}/input")

    basedir = Path(__file__).parent
    input_filename = basedir / str(year) / f"{day}_input.txt"
    solution_py_filename = basedir / str(year) / f"{day}.py"

    # Wait for puzzle start
    puzzle_start = datetime.fromisoformat(f"{year}-12-{day:02}T05:00:01+00:00").astimezone()
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
    logger.info("Scaffolding puzzle at %s", day_url)

    if not input_filename.exists():
        input_filename.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Getting input from %s", input_url)
        with s.get(input_url) as u:
            if u.text.startswith("Please don't"):
                logger.error("Puzzle not available yet!")
                return
            with input_filename.open("w") as input_txt:
                input_txt.write(u.text)

    if not solution_py_filename.exists():
        logger.info(f"Generating code scaffold for day {day}")
        code = make_scaffold()
        with solution_py_filename.open("w") as solution_py:
            solution_py.write(code)


def make_scaffold() -> str:
    basedir = Path(__file__).parent

    with (basedir / "templates" / "solution_template.py").open() as tmpl:
        code = tmpl.read()

    return code


if __name__ == "__main__":
    main()
