from datetime import datetime, timedelta
import json
from pathlib import Path
from yachalk import chalk
import click

from aoc.util import (
    create_session,
    leaderboard_id,
    leaderboard_year,
    me,
    session_cookie,
    leaderboard_url,
)

ME = me()
FUTURE_TS = (datetime.now() + timedelta(days=1)).timestamp()


@click.command()
@click.option("--day", metavar="DAY", help="sort by completion of DAY")
@click.option("--count", metavar="N", help="print the top N entries", default=30)
def main(day: int | None, count: int):
    """
    Prints a private Advent of Code (https://adventofcode.com/) leaderboard"""

    if session_cookie() is None:
        print("SESSION_COOKIE enviroment variable not set")
        return

    directory = Path(__file__).parent.parent / ".leaderboard_cache"
    directory.mkdir(exist_ok=True)

    board_id = leaderboard_id()
    year = leaderboard_year()
    if not year or not board_id:
        return

    file = directory / f"{board_id}_{year}.json"

    if file.exists() and datetime.fromtimestamp(file.stat().st_mtime) + timedelta(minutes=15) > datetime.now():
        print(f"Using cache dated {datetime.fromtimestamp(file.stat().st_mtime)}")
        with open(file) as fp:
            contents = json.load(fp)
    else:
        url = leaderboard_url(board_id, year)
        s = create_session()
        r = s.get(url)

        contents = r.json()

        # Write cache
        with open(file, "w") as fp:
            json.dump(contents, fp, indent=2)

    last_calendar_day = datetime(year=year, month=12, day=25)
    today = min(last_calendar_day, datetime.now()).day

    if day is None:
        sort_fn = sort_by_local_score
        day = today
    else:
        sort_fn = sort_by_day(day)
    members = sorted(contents["members"].values(), key=sort_fn, reverse=True)

    calculate_stars_str(members, today)

    found_me = False
    for i, m in enumerate(members):
        name = (m["name"] or str(m["id"]))[:20]
        if name == ME:
            name = chalk.green(name)
            found_me = True
        else:
            name = chalk.white(name)

        day_completion = m["completion_day_level"].get(str(day), dict())
        part1_ts = day_completion.get("1", {}).get("get_star_ts", None)
        part2_ts = day_completion.get("2", {}).get("get_star_ts", None)
        part1_time = datetime.fromtimestamp(part1_ts).time() if part1_ts else "---"
        part2_time = datetime.fromtimestamp(part2_ts).time() if part2_ts else "---"
        score = m["local_score"]
        stars = m["stars_str"]
        print(f"{i+1:3} {score:5} {name:30} {stars:50} {part1_time}  {part2_time}")

        if (ME is None or found_me) and i + 1 >= count:
            break


def calculate_stars_str(members, day):
    for i, m in enumerate(members):
        m["stars_str"] = ""

    for d in range(1, day + 1):
        for part in ["1", "2"]:
            ranked = sorted(
                members,
                key=lambda m, part=part: m["completion_day_level"]
                .get(str(d), {})
                .get(part, {})
                .get("get_star_ts", FUTURE_TS),
            )
            for i, m in enumerate(ranked):
                if not m["completion_day_level"].get(str(d), {}).get(part, {}).get("get_star_ts", False):
                    m["stars_str"] += "-"
                elif i < 10:
                    m["stars_str"] += str(i + 1)[-1]
                else:
                    m["stars_str"] += "*"


def sort_by_local_score(m):
    return m["local_score"]


def sort_by_day(day: int):
    def sort(m):
        silver_star_ts = m["completion_day_level"].get(str(day), dict()).get("1", {}).get("get_star_ts", FUTURE_TS)
        gold_star_ts = m["completion_day_level"].get(str(day), dict()).get("2", {}).get("get_star_ts", FUTURE_TS)
        return -gold_star_ts, -silver_star_ts, m["local_score"]

    return sort


if __name__ == "__main__":
    main()
