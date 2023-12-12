import os
from typing import Optional, cast
from bs4.element import Tag
from markdownify import MarkdownConverter
from bs4 import BeautifulSoup
import textwrap
from dotenv import load_dotenv
import requests


load_dotenv()


class MyConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """

    def convert_p(self, el, text, convert_as_inline):
        p = textwrap.fill(super().convert_p(el, text, convert_as_inline)) + "\n"
        return p

    def convert_li(self, el, text, convert_as_inline):
        li = textwrap.fill(super().convert_li(el, text, convert_as_inline)) + "\n"
        return li


def convert_tag_to_md(full_html: str, tag: str, index=1) -> Optional[str]:
    soup = BeautifulSoup(full_html, "html.parser")
    matching_tags = soup.find_all(tag, limit=index)

    if len(matching_tags) < index:
        return None

    description = cast(Tag, matching_tags[index - 1]).decode_contents()

    return MyConverter(heading_style="ATX").convert(description).strip()


def create_session():
    s = requests.session()
    s.cookies.set("session", session_cookie())
    s.headers["User-Agent"] = "github.com/estyrke/AoC by emil.styrke@gmail.com"
    return s


def session_cookie():
    return os.getenv("SESSION_COOKIE")


def me():
    return os.getenv("ME")


def base_url():
    return "https://adventofcode.com"


def leaderboard_url(board_id: str, year: int):
    return f"https://adventofcode.com/{year}/leaderboard/private/view/{board_id}.json"


def leaderboard_year() -> int:
    year = os.getenv("PRIVATE_LEADERBOARD_YEAR")
    if year is None:
        print("PRIVATE_LEADERBOARD_YEAR environment variable is not set!")
        return 0
    return int(year)


def leaderboard_id() -> str:
    board_id = os.getenv("PRIVATE_LEADERBOARD_ID")
    if board_id is None:
        print("PRIVATE_LEADERBOARD_ID environment variable is not set!")
        return ""
    return board_id
