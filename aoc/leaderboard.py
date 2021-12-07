import requests
from datetime import datetime, timedelta
from yachalk import chalk

from aoc.util import me, session_cookie, leaderboard_url

ME = me()


def main():
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

    members = sorted(
        json["members"].values(), key=lambda m: m["local_score"], reverse=True
    )
    day = datetime.now().day

    calculate_rank_str(members, day)

    found_me = False
    for i, m in enumerate(members):
        name = (m["name"] or m["id"])[:20]
        if name == ME:
            name = chalk.green(name)
            found_me = True
        else:
            name = chalk.white(name)
        completion_today = m["completion_day_level"].get(str(day), dict())
        part1_ts = completion_today.get("1", {}).get("get_star_ts", None)
        part2_ts = completion_today.get("2", {}).get("get_star_ts", None)
        part1_time = datetime.fromtimestamp(part1_ts).time() if part1_ts else "---"
        part2_time = datetime.fromtimestamp(part2_ts).time() if part2_ts else "---"
        print(
            f"{i+1:3} {m['local_score']:4} {name:30} {m['rank_str']:50} {part1_time}  {part2_time}"
        )

        if (ME is None or found_me) and i >= 100:
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
                .get("get_star_ts", (datetime.now() + timedelta(days=1)).timestamp()),
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


if __name__ == "__main__":
    main()
