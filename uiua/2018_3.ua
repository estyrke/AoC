~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Parse ← ≡(≡⋕{°$"#_ @ _,_: _x_"}) ⊜□≠, @\n
Input ← AoCGet 2018 3
Part₁ ← ⧻▽⊸(>1)⊕⧻⊛.∧(
  ⊂♭₂⊞⊂⊃(+⇡:⊙⋅∘|+⇡:⋅⊙⋅∘)⊢₄↘1
): [] Parse

# From the parsed input, return the claim ID for each coordinate and a classification id of each coordinate
IDsClassifiedByCoordinates ← ⊙♭⊛⍜(⍉)⊃(↙2|↘2) ∧(
  ⊂⍜⍉⊂♭₂⊞⊂⊃(+⇡:⋅⊙⋅∘|+⇡:⋅⋅⊙⋅∘|∘)⊢₅
) :[]

Part₂ ← ⊢▽¬⊸∊?⊙(♭≡(↙1))◴∧(⊂°□):[]▽≡(
  >1⧻°□
).⊕□IDsClassifiedByCoordinates.Parse

┌─╴test
  ⍤⤙≍ [1_1_3_4_4 2_3_1_4_4 3_5_5_2_2] Parse $ #1 @ 1,3: 4x4
                                            $ #2 @ 3,1: 4x4
                                            $ #3 @ 5,5: 2x2
  ⍤⤙≍ 4 Part₁ $ #1 @ 1,3: 4x4
              $ #2 @ 3,1: 4x4
              $ #3 @ 5,5: 2x2
  # ⍤⤙≍ 3 Part₂ $ #1 @ 1,3: 4x4
  #            $ #2 @ 3,1: 4x4
  #            $ #3 @ 5,5: 2x2
└─╴

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
⍜now IDsClassifiedByCoordinates.Parse Input
# $"Part 2 returned _ after _ sec":
⍜now Part₂ Input
