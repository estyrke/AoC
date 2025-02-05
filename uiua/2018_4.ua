~ "git: github.com/amatgil/steal-gift" ~ AoCGet

$ [1518-11-01 00:00] Guard #10 begins shift
$ [1518-11-01 00:05] falls asleep
$ [1518-11-01 00:25] wakes up
$ [1518-11-01 00:30] falls asleep
$ [1518-11-01 00:55] wakes up
$ [1518-11-01 23:58] Guard #99 begins shift
$ [1518-11-02 00:40] falls asleep
$ [1518-11-02 00:50] wakes up
$ [1518-11-03 00:05] Guard #10 begins shift
$ [1518-11-03 00:24] falls asleep
$ [1518-11-03 00:29] wakes up
$ [1518-11-04 00:02] Guard #99 begins shift
$ [1518-11-04 00:36] falls asleep
$ [1518-11-04 00:46] wakes up
$ [1518-11-05 00:03] Guard #99 begins shift
$ [1518-11-05 00:45] falls asleep
$ [1518-11-05 00:55] wakes up
TestInput ←

Input ← AoCGet 2018 4

Preparse ← ≡(°□⬚¯1↘1{∩₄⋕°$"[1518-_-_ _:_] _"})⍆ ⊜□≠, @\n
Parse    ← ≡(≡°□⊃(⍜(°□⊣)⍣(⋕°$"Guard #_ begins shift"|¯1°$"wakes up"|¯2°$"falls asleep"))) Preparse

# Given a list of events for a single night, return the guard id and a 60-length array where 0 means awake and 1 means asleep in that minute.
CountMinutes ← ⊃(
  ⊣⊣↙1 # Guard number, last element of first row
| ∧(
    ⊃(-1¯⊣|⊢↘2) # Extract the action (-1 = wake up, -2 = falls asleep), and the minute
    ⨬(+1⊚-:⊙⊸⧻  # wakes up, make array of 1s since last sleep
    | ⊚-:⊙⊸⧻    # falls asleep, make array of 0s since last wake up
    )
    ⊂: # Append the minute to the array
  ): [] ↘1
  +⊚⊃(-:60⧻|¬⍣⊣1|∘) # Pad the array to 60 minutes with the inverse of the last action
  ⊂:                # Append the final minutes
)

Part₁ ← ⊡⊢⍖⊙(/×⊟):⊙⊕⊃(
  /+/+   # Total slept minutes
| ⊗/↥./+ # Minute most asleep
)⤚⊕⊢⊸⊛⊜CountMinutes\+≥0≡⊣ . Parse

Part₂ ← ⊡⊢⍖⊙(/×⊟):⊙⊕(
  ⊙⊗./↥./+ # Minute most asleep, and times slept that minute
) ⤚⊕⊢⊸⊛⊜CountMinutes\+≥0≡⊣ . Parse

┌─╴test
  ⍤⤙≍ [{1 0 0 "Guard #10 begins shift"}]↙ 1 Preparse TestInput
  ⍤⤙≍ [[1 0 0 10]]↙ 1 Parse TestInput
  ⍤⤙≍ 240 Part₁ TestInput
  ⍤⤙≍ 4455 Part₂ TestInput
└─╴

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
$"Part 2 returned _ after _ sec":⍜now Part₂ Input
