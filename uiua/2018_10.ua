$ position=< 9,  1> velocity=< 0,  2>
$ position=< 7,  0> velocity=<-1,  0>
$ position=< 3, -2> velocity=<-1,  1>
$ position=< 6, 10> velocity=<-2, -1>
$ position=< 2, -4> velocity=< 2,  2>
$ position=<-6, 10> velocity=< 2, -2>
$ position=< 1,  8> velocity=< 1, -1>
$ position=< 1,  7> velocity=< 1,  0>
$ position=<-3, 11> velocity=< 1, -2>
$ position=< 7,  6> velocity=<-1, -1>
$ position=<-2,  3> velocity=< 1,  0>
$ position=<-4,  3> velocity=< 2,  0>
$ position=<10, -3> velocity=<-1,  1>
$ position=< 5, 11> velocity=< 1, -2>
$ position=< 4,  7> velocity=< 0, -1>
$ position=< 8, -2> velocity=< 0,  1>
$ position=<15,  0> velocity=<-2,  0>
$ position=< 1,  6> velocity=< 1,  0>
$ position=< 8,  9> velocity=< 0, -1>
$ position=< 3,  3> velocity=<-1,  1>
$ position=< 0,  5> velocity=< 0, -1>
$ position=<-2,  2> velocity=< 2,  0>
$ position=< 5, -2> velocity=< 1,  2>
$ position=< 1,  4> velocity=< 2,  1>
$ position=<-2,  7> velocity=< 2, -2>
$ position=< 3,  6> velocity=<-1, -1>
$ position=< 5,  0> velocity=< 1,  0>
$ position=<-6,  0> velocity=< 2,  0>
$ position=< 5,  9> velocity=< 1, -2>
$ position=<14,  7> velocity=<-2,  0>
$ position=<-3,  6> velocity=< 2, -1>
TestInput ←

Parse ← ⊜([∩₄⋕ °$"position=<_,_>velocity=<_,_>"]) ⊸≠@\n▽⊸≠@\s

ChaosIndex ← +⊃(/+◰≡⊡₀|/+◰≡⊡₁) # Get the sum of unique x and y coordinates
GridSize ← (
  ≡↙2
  /×-⊃/↧/↥
)
Render ← &ims . >0 °⊚ -¤⊸/↧≡(⇌↙₂)
Solve ← (
  :¯1
  ⊸GridSize
  ⍢( # ⍥(Render.) <⊙⧻ ⊸GridSize
    ⊙⊙+₁
    ⊙≡(⬚0+⊸↙¯2)
  | ⊸≤⊙⊸GridSize)
  ◌
  ≡(⬚0-⊸↙¯2) # Reverse the last step
)

Part₁ ← (
  Parse
  Solve
  Render
)

┌─╴test
  /$"_\n_" ⨬@.@# Part₁ TestInput
  ⍤⤙≍ $ #...#..###
      $ #...#...#.
      $ #...#...#.
      $ #####...#.
      $ #...#...#.
      $ #...#...#.
      $ #...#...#.
      $ #...#..###
  ⍤⤙≍ 3
└─╴

Part₂ ← (
  Parse
  Solve
)

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 10

$"Part 1 returned after _ sec" ⊙◌ ⍜now Part₁ Input
$"Part 2 returned _" ⤙⊙◌
