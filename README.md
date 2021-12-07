# My Advent of Code solutions

## Helper scripts

There are some scripts to help me. They require some environmennt variables, that can preferably be set by creating a `.env` file in the repo root with the following contents:

```
SESSION_COOKIE=<adventofcode.com session cookie>
ME=<own name as it appears in private leaderboard>
PRIVATE_LEADERBOARD_ID=<id of private leaderboard>
PRIVATE_LEADERBOARD_YEAR=<year of leaderboard>
```

### `aoc_get`

`aoc_get <year> <day>` downloads the description and input for the given day and creates code skeletons for parts 1 (and 2 if available).

### `aoc_run`

`aoc_run <year> <day> <part>` runs a given solution and posts the answer to the site.

`aoc_run <year> <day> <part> test` runs a given solution and prints the computed answer but does not post it.

### `aoc_leaderboard`

`aoc_leaderboard [day]` fetches and prints a private leaderboard specified in the `.env` file. If no day is given, sorts by local score, else sorts by gold star time for the given day.
