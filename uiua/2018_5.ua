~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input     ← AoCGet 2018 5
TestInput ← "dabAcCaCBAcCcaDA"

Part₁ ← ⧻∧(⨬(⊂¯|↘1◌)⍣(⤚=¯⊙⊸⊢|0¯)): ""
Part₂ ← (
  ⍆▽⊸◰⌵. # Find unique parts
  ⊙¤     # Fix original string into array
  ≡(     # For each unique part, remove it and run Part₁ on the rest
    Part₁ ▽≠⌵,
  )
  ⊢/↧ # Get the smallest result
)
┌─╴test
  ⍤⤙≍ 10 Part₁ TestInput
  ⍤⤙≍ 4 Part₂ TestInput
└─╴

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
$"Part 2 returned _ after _ sec":⍜now Part₂ Input
