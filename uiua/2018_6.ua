$ 1, 1
$ 1, 6
$ 8, 3
$ 3, 4
$ 5, 5
$ 8, 9
TestInput ←

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 6

Parse ← (
  ⊜(
    ▽⊸≠@   # Remove whitespace
    ⊜⋕⊸≠@, # Split by comma
  ) ⊸≠@\n  # Split by newline
)
MinMax ← ∩(⍜-(⇡+1)°⊟)°⊟⍉⊟⊃/↧/↥
Part₁ ← (
  MinMax ⟜¤ Parse # Parse input and get min->max ranges for x and y
  ⊞(              # Make a table from the x and y ranges
    ≡/+⌵⊸-¤⊟      # For each point, calculate the Manhattan distance to each coordinate
    =0/-∩(↙2)⊃⍆⍏  # Take the two closest coordinates and check if they are at the exact same distance
    ⨬(⊡⊢|[¯1 ¯1]) # If they aren't, pick the closest coordinate, else return [-1 -1]
  )
  ⊃(⊕(⊂⊃⧻⊢)⊸⊛♭₂         # Count how many times each point appear in the grid
  | ¤▽⊸◰⊂⊂⊂⊃(⊢|⊣|≡⊢|≡⊣) # Find all coordinates that are on the edge of the grid - they are infinite and should be ignored
  )
  ▽⤚≡(=⊗⊓(↘₁|⟜⧻≡♭)) # Discard all infinite coordinates
  ⊢⊡⊢⊸⍖             # Return the maximum value
)

Part₂ ← (
  ⊙(MinMax ⟜¤ Parse)
  ⊙⊞(
    /+≡/+⌵-¤⊟ # For each point, calculate the Manhattan distance to each coordinate
  )
  <   # Find points less than threshold
  /+♭ # Count them
)

┌─╴test
  ⍤⤙≍ 17 Part₁ TestInput
  ⍤⤙≍ 16 Part₂ 32 TestInput
└─╴

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
$"Part 2 returned _ after _ sec":⍜now Part₂ 10000 Input
