from datetime import datetime
from io import StringIO
from aoc.get import get

from aoc.legacy_runner import LegacyRunner
from . import log
import os
import sys
import importlib
from time import sleep
from types import ModuleType
from typing import Optional
from urllib.parse import urljoin
import traceback


from aoc.util import base_url, convert_tag_to_md, create_session

logger = log.getLogger(__name__)


class Runner:
    def __init__(self, year: int, day: int, part: int):
        basedir = os.path.dirname(__file__)
        self.solution_filename = f"{basedir}/{year}/{day}.py"
        self.input_filename = f"{basedir}/{year}/{day}_input.txt"
        self.answer_url = urljoin(base_url(), f"{year}/day/{day}/answer")
        self.mod_name = f"aoc.{year}.{day}"

        self.year = year
        self.day = day
        self.part = part

        if not os.path.exists(self.solution_filename):
            get(year, day)

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

            self.post_answer(answer)

    def post_answer(self, answer):
        s = create_session()
        logger.info(f"Posting answer {answer} to {self.answer_url}")
        with s.post(self.answer_url, data={"level": self.part, "answer": answer}) as u:
            print(convert_tag_to_md(u.text, "article"))

    def try_load(self, mod_name):
        try:
            mod = importlib.import_module(mod_name)
            importlib.reload(mod)
        except SyntaxError:
            traceback.print_exc()
            return None
        return mod

    def run_once(self, mod_name: str):
        mod = self.try_load(mod_name)
        if mod is None:
            return None

        test_ok = self.run_test(mod)

        if test_ok is False:
            return None

        if self.part == 2 and self.answer_part_1 is None:
            self.answer_part_1 = self.run_real(mod, 1)

        answer = self.run_real(mod, self.part)

        if self.part == 2 and answer == self.answer_part_1:
            logger.warning(
                f"Answer {answer} for part 2 is the same as for part 1 - NOT posting!"
            )
            return None
        return answer

    def run_test(self, mod: ModuleType) -> Optional[bool]:
        test_input = getattr(mod, f"part{self.part}_test_input", None)
        test_output = getattr(mod, f"part{self.part}_test_output", None)

        if not test_input:
            return None

        assert isinstance(test_input, str)

        # The real input always ends with a newline, so ensure the test input does too
        if not test_input.endswith("\n"):
            test_input = test_input + "\n"

        test_ok = None
        try:
            mod.__dict__["IS_TEST"] = True
            test_answer = mod.__dict__[f"part{self.part}"](StringIO(test_input))
        except KeyboardInterrupt:
            logger.warning("Interrupted")
            test_ok = False
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

    def run_real(self, mod: ModuleType, part: int):
        answer = None
        with open(self.input_filename) as inp:
            try:
                mod.__dict__["IS_TEST"] = False
                answer = mod.__dict__[f"part{part}"](inp)
            except KeyboardInterrupt:
                logger.warning("Interrupted!")
            except Exception:
                logger.error(traceback.format_exc())

        if answer is not None:
            logger.info(f"Part {part} answer is {answer}")
        else:
            logger.warning("No answer...")
        return answer

    def wait_for_change(self, prev_mtime: Optional[datetime]) -> datetime:
        while True:
            st = os.stat(self.solution_filename)
            mtime = datetime.fromtimestamp(st.st_mtime)

            if mtime != prev_mtime:
                return mtime
            sleep(1)


def main():
    log.init_logging()
    year = int(sys.argv[1])
    day = int(sys.argv[2])
    part = int(sys.argv[3])
    test = len(sys.argv) >= 5 and sys.argv[4] == "test"

    if year in [2020, 2021]:
        # 2021 and 2020 used a different file layout (I have been doing AoC
        # retroactively "backwards" from 2021)
        return LegacyRunner(year, day, part).run(test, True)

    Runner(year, day, part).run(test, True)


if __name__ == "__main__":
    main()
