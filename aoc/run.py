from datetime import datetime
from io import StringIO
from . import logging
import os
import sys
import importlib
from time import sleep
from types import ModuleType
from typing import Optional
from urllib.parse import urljoin
import traceback

import requests

from aoc.util import base_url, convert_tag_to_md, session_cookie
from aoc.get import get


logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, year: int, day: int, part: int):
        basedir = os.path.dirname(__file__)
        self.part_filename = f"{basedir}/{year}/{day}_{part}.py"
        self.input_filename = f"{basedir}/{year}/{day}_input.txt"
        self.answer_url = urljoin(base_url(), f"{year}/day/{day}/answer")
        self.mod_name = f"aoc.{year}.{day}_{part}"
        mod_name_part_1 = f"aoc.{year}.{day}_1"

        self.year = year
        self.day = day
        self.part = part

        if not os.path.exists(self.part_filename):
            get(year, day)

        if part == 2:
            mod_part_1 = importlib.import_module(mod_name_part_1)

            self.answer_part_1 = self.run_real(mod_part_1)
        else:
            self.answer_part_1 = None

    def run(self, test, watch):
        if not watch:
            answer = self.run_once(self.mod_name)
        else:
            answer = None
            mtime = None
            while answer is None:
                mtime = self.wait_for_change(mtime)
                answer = self.run_once(self.mod_name)

        if answer is not None:
            if test:
                logger.warning(f"NOT posting answer {answer}")
                return

            self.post_and_get_next(answer)

    def post_and_get_next(self, answer):
        s = requests.session()
        s.cookies.set("session", session_cookie())
        logger.info(f"Posting answer {answer} to {self.answer_url}")
        with s.post(self.answer_url, data={"level": self.part, "answer": answer}) as u:
            print(convert_tag_to_md(u.text, "article"))
            if self.part == 1 and "That's the right answer" in u.text:
                # Download part 2
                get(self.year, self.day)

    def run_once(self, mod_name: str):
        try:
            mod = importlib.import_module(mod_name)
            importlib.reload(mod)
        except SyntaxError:
            traceback.print_exc()
            return None

        test_ok = self.run_test(mod)

        if test_ok == False:
            return None
        answer = self.run_real(mod)

        if self.part == 2 and answer == self.answer_part_1:
            logger.warning(
                f"Answer {answer} for part 2 is the same as for part 1 - NOT posting!"
            )
            return None
        return answer

    def run_test(self, mod: ModuleType) -> Optional[bool]:
        test_input = getattr(mod, "test_input", None)
        test_output = getattr(mod, "test_output", None)

        if not test_input:
            return None

        test_ok = None
        try:
            test_answer = mod.solve(StringIO(mod.test_input))
        except Exception:
            traceback.print_exc()
            test_ok = False
        else:
            if test_output is not None and test_answer == test_output:
                logger.info(f"Test answer was {test_answer} (OK!)")
                test_ok = True
            elif test_output is not None and test_answer != test_output:
                logger.error(f"Test answer was {test_answer}, expected {test_output}")
                test_ok = False
            elif test_output is None and test_answer is not None:
                logger.info(f"Test answer was {test_answer}")
        return test_ok

    def run_real(self, mod: ModuleType):
        answer = None
        with open(self.input_filename) as inp:
            try:
                answer = mod.solve(inp)
            except KeyboardInterrupt:
                logger.warning("Interrupted!")

        if answer is not None:
            logger.info(f"Answer is {answer}")
        else:
            logger.warning("No answer...")
        return answer

    def wait_for_change(self, prev_mtime: Optional[datetime]) -> datetime:
        while True:
            st = os.stat(self.part_filename)
            mtime = datetime.fromtimestamp(st.st_mtime)

            if mtime != prev_mtime:
                return mtime
            sleep(1)


def main():
    logging.init_logging()
    year = int(sys.argv[1])
    day = int(sys.argv[2])
    part = int(sys.argv[3])
    test = len(sys.argv) >= 5 and sys.argv[4] == "test"
    Runner(year, day, part).run(test, True)


if __name__ == "__main__":
    main()
