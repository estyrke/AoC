Parse ← ∩⋕ °$"_ players; last marble is worth _ points"

Play ← (
  ⊚
  0
  :[0]
  ⤙⊙⊙⊙◌
  ⍥(|3.3.+1
        =0◿10000. # Every 10000th marble ...
        ⍥(&p.)    # ... print the marble, just to track progress
        =0◿23.
        ⨬(
      ⊙⊙(⊓(↻2|↻1))
      ⊙⊂:
    | ⊙⊙(⊓(↻¯7|↻1))
      ⍜⊙⋅⋅∘ (⬚0+¤)
      ⍜◌(⊙⬚0+⊃↘₁↙₁)
    )
  )
  /↥◌◌)

# Experimental!
┌─╴Circle
  ~{
    Current ← 0
    Next ← 1
    Buf ← [⍥0_0_0]
  }

  # Insert a new marble in the circle
  # Circle ? NewValue Circle
  Insert ← (
    ⍜now(
      :
      ⟜⊃(
        $Current Circle~Current
      | $Next Circle~Next)
      ⍜Circle~Buf(
        ⍜(⊡)(⍜⊡₂(⤙⊙⊙∘ $OldNext)) ⤙⊙∘ # Set the current.next to next. Returns buf and old next
        ⍜(⊡)(⍜⊡₁(⤙⊙⊙∘◌)) ⤙⊙∘         # Set the OldNext.prev to next.
        ⍜(⊡)(⊂:⊂: ⊙⊙: ◌) ⤙⊙⊙⊙∘       # Set the Next element to [NewValue Current OldNext]
      )
      ⍜Current(◌) # Set the Current pointer to Next
      ⍜Next+₁     # Increment Next
    )
    ◌ # &p $"Insert took _ sec"
  )

  # Rotate the circle by a given number of steps
  # Circle ? Steps Circle
  ~Rotate ← (
    ⊃(>0|⌵)
    ⨬(⍥(⍜Current(⊡₁⊡ :Buf)) # If steps is negative, follow the prev pointers
    | ⍥(⍜Current(⊡₂⊡ :Buf)) # If steps is positive, follow the next pointers
    )
    Self
  )

  # Pop the current marble from the circle
  # Value Circle ? Circle
  ~Pop ← (
    ⍜Buf(
      ⍜(⊡)(0_0_0) Current # Set the current.next to next. Returns buf and old next
      ⊃(
        ⍜⊡(⍜⊡₁(⊡₁.◌)) ⊡₂⤙⊙∘ # Set next.prev to prev
        ⍜⊡(⍜⊡₂(⊡₂.◌)) ⊡₁⤙⊙∘ # Set prev.next to next
      )
    )
    ⍜Current (⊡₂.◌) # Set current to next
    ⊢               # Return the value

    Self
  )

  ┌─╴test
    ⍤⤙≍ {2 3 [0_2_1 5_0_2 17_1_0 0_0_0]} . Circle~Insert 17 Circle~Insert 5 Circle 4
    ⍤⤙≍ {0 3 [0_2_1 5_0_2 17_1_0 0_0_0]} Circle~Rotate 1 .
    ⍤⤙≍ {0 3 [0_2_1 5_0_2 17_1_0 0_0_0]} Circle~Rotate ¯2 .
    ⍤⤙≍ {1 3 [0_2_1 5_0_2 17_1_0 0_0_0]} Circle~Rotate ¯1 .
    ⍤⤙≍ {1 3 [0_2_1 5_0_2 17_1_0 0_0_0]} Circle~Rotate 2 .
    ⍤⤙≍ {{0 3 [0_1_1 5_0_0 0_0_0 0_0_0]} 17} □₂ Circle~Pop
  └─╴
└─╴

# Alternative version. This was supposed to be more efficient, but actually is way slower.
# Circle~Insert is the bottleneck, presumably it makes copies of the buffer, while it needs to be zero-copy to be efficient.
Play₂ ← (
  ⊓($Scores ⊚)(Circle.)
  $Marble 0
  $MarbleCount ⤙⊙⊙⊙◌ # Pull out the count
  ⍥(+1
    ⍜now(
      =0◿10000. # Every 10000th marble ...
      ⍥(&p.)    # ... print the marble, just to track progress
      =0◿23.
      ⨬(⊙(↻ 1)                  # Rotate the scores by 1
        ⊙⊙(Circle~Rotate 1)     # Rotate the circle by 2
        ⊃(⊙∘|Circle~Insert ⊙⋅∘) # Insert the new marble
      |                         # ⊙(⊓(↻¯7|↻1))
        # ⍜⊙⋅⋅∘ (⬚0+¤)
        # ⍜◌(⊙⬚0+⊃↘₁↙₁)
        ⊙(↻ 1)               # Rotate the scores by 1
        ⊙⊙(Circle~Rotate ¯7) # Rotate the circle by -7
        ⊙⊙(Circle~Pop)       # Pop the marble
        ⊙(⍜⊡₀+ :⤙⊙⊙◌)        # Add popped marble...
        ⟜(⍜⊡₀+ :)            # ...and current marble to current score
      )
    )
    ◌ # &p $"Play took _ sec"
  )
  /↥⋅⊙◌
)

Part₁ ← (
  Parse
  Play
)
┌─╴test
  ⍤⤙≍ 32 Part₁ "9 players; last marble is worth 25 points"
  ⍤⤙≍ 8317 Part₁ "10 players; last marble is worth 1618 points"
  ⍤⤙≍ 146373 Part₁ "13 players; last marble is worth 7999 points"
  ⍤⤙≍ 2764 Part₁ "17 players; last marble is worth 1104 points"
  ⍤⤙≍ 54718 Part₁ "21 players; last marble is worth 6111 points"
  ⍤⤙≍ 37305 Part₁ "30 players; last marble is worth 5807 points"
└─╴

Part₂ ← (
  Parse
  ⊙×₁₀₀
  Play
)

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 9

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
# $"Part 2 returned _ after _ sec":⍜now Part₂ Input
# "Part 2 returned 3628143500 after 52521.35272312164 sec"
# \(÷:) ⊂: [60 60 24] 52521.35272312164
