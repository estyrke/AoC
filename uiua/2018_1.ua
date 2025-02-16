~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 1

Parse ← ⋕ ⊜□≠, @\n
Part₁ ← /+Parse
Part₂ ← (
  Parse
  ⍢(⊂ ⟜(+⊣)⊙(⊸\+))⊸(/×◰) [0] # While all elements are unique, create a new frequency list from the start array and append it
  ⊡ ⊢ ⊚ ¬ ⊸◰                 # Get the first duplicate
  ⊙◌                         # Drop the frequency changes from the stack
)

┌─╴test
  ⍤ ⤙≍ 574 Part₁ Input
  ⍤ ⤙≍ 0 Part₂ "+1\n-1\n-1\n+1"
  ⍤ ⤙≍ 1 Part₂ "+1\n+1\n-1\n+1"
  ⍤⤙≍ 10 Part₂ "+3\n+3\n+4\n-2\n-4"
  ⍤⤙≍ 5 Part₂ "-6\n+3\n+8\n+5\n-6"
  ⍤⤙≍ 14 Part₂ "+7\n+7\n-2\n-7\n-4"
└─╴

$"Part 1 returned _ in _ sec" : ⍜now (Part₁ Input)
$"Part 2 returned _ in _ sec" : ⍜now (Part₂ Input)
