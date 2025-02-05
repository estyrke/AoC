Input ← &fras?⊡ 1 &args
Parse ← ⋕ ⊜□≠, @\n
Part₁ ← /+Parse
PartOld₂ ← ⍢(
  ⊃((+⊢):⊙⋅∘
  | ⋅∘
  | ⋅⋅(↻1)
  )
| ⊃(=¯1⬚¯1⊗|⟜⊂)
) 0 [] Parse

Part₂ ← ⊡ ⊢ ⊚ ¬ ⊸◰ ?⍢(⊂ ⟜(+⊣)⊙(⊸\+))⊸(/×◰) [0] Parse
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
# ⍜now (PartOld₂ Input)
# ⊕(⧻) ?⊛. Input
