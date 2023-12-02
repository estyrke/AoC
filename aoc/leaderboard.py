import requests
from datetime import datetime, timedelta
from yachalk import chalk
import click

from aoc.util import leaderboard_year, me, session_cookie, leaderboard_url

ME = me()
FUTURE_TS = (datetime.now() + timedelta(days=1)).timestamp()


@click.command()
@click.option("--day", metavar="DAY", help="sort by completion of DAY")
@click.option("--count", metavar="N", help="print the top N entries", default=30)
def main(day: int, count: int):
    """
    Prints a private Advent of Code (https://adventofcode.com/) leaderboard"""

    s = requests.session()
    if session_cookie() is None:
        print("SESSION_COOKIE enviroment variable not set")
        return
    s.cookies.set("session", session_cookie())

    url = leaderboard_url()
    if url is None:
        return

    r = s.get(url)

    json = r.json()

    last_calendar_day = datetime(year=leaderboard_year(), month=12, day=25)
    today = min(last_calendar_day, datetime.now()).day

    if day is None:
        sort_fn = lambda m: m["local_score"]
        day = today
    else:
        sort_fn = sort_by_day(day)
    members = sorted(json["members"].values(), key=sort_fn, reverse=True)

    calculate_rank_str(members, today)

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
        print(
            f"{i+1:3} {m['local_score']:4} {name:30} {m['rank_str']:50} {part1_time}  {part2_time}"
        )

        if (ME is None or found_me) and i + 1 >= count:
            break


def calculate_rank_str(members, day):
    for i, m in enumerate(members):
        m["rank_str"] = ""

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
                if (
                    not m["completion_day_level"]
                    .get(str(d), {})
                    .get(part, {})
                    .get("get_star_ts", False)
                ):
                    m["rank_str"] += "-"
                elif i < 10:
                    m["rank_str"] += str(i + 1)[-1]
                else:
                    m["rank_str"] += "*"


def sort_by_day(day: int):
    def sort(m):
        silver_star_ts = (
            m["completion_day_level"]
            .get(str(day), dict())
            .get("1", {})
            .get("get_star_ts", FUTURE_TS)
        )
        gold_star_ts = (
            m["completion_day_level"]
            .get(str(day), dict())
            .get("2", {})
            .get("get_star_ts", FUTURE_TS)
        )
        return -gold_star_ts, -silver_star_ts, m["local_score"]

    return sort


if __name__ == "__main__":
    main()
