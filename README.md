# My Advent of Code solutions

Most of these are as I wrote them initially (trying to be as fast as I can), meaning the code is really yucky. Some are written with less time pressure,
especially everything 2020 and before (I did not participate "in real time" before 2021), and may look nicer.

Some solutions have been modified after the fact, this may or may not be indicated in the commit messages.

## Helper scripts

There are some scripts to help me. They require some environment variables; they can be set by creating a `.env` file in the repo root with the following contents:

```
SESSION_COOKIE=<adventofcode.com session cookie>
ME=<own name as it appears in private leaderboard>
PRIVATE_LEADERBOARD_ID=<id of private leaderboard>
PRIVATE_LEADERBOARD_YEAR=<year of leaderboard>
```

These scripts follow the automation guidelines on the [/r/adventofcode community wiki](https://www.reddit.com/r/adventofcode/wiki/faqs/automation). Specifically:

- Outbound calls are only made manually as part of submission and initial input download. The leaderboard script caches the data it downloads for 15 minutes.
- Once inputs are downloaded, they are cached locally on disk. If you suspect your input is corrupted, you can force a new download by deleting the corresponding input file.
- The `User-Agent` header in `aoc.util.create_session()` is set to me since I maintain this repo.

### `aoc_get`

`aoc_get <year> <day>` downloads the input for the given day and creates a code skeleton.

### `aoc_run`

`aoc_run <year> <day> <part>` runs a given solution (downloading first if not existing) and eventually posts the answer to the site. The script watches for changes in the solution file and tries to run it after every save. For a solution to be posted, it must pass the following conditions:

- It runs to completion
- It returns the correct response for the example given in the solution file (`part_<n>_test_input` should result in `part_<n>_test_output`). Note: if `part_<n>_test_output` is `None`, no such test will be performed
- For part two, it returns a different result than part 1 (to avoid accidentally submitting copy/pasted part 1)

`aoc_run <year> <day> <part> test` runs a given solution and prints the computed answer but does not post it.

### `aoc_leaderboard`

`aoc_leaderboard` fetches and prints a private leaderboard specified in the `.env` file. See `aoc_leaderboard --help` for options.
