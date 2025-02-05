~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Parse ← ⊜□≠, @\n
Input ← AoCGet 2018 2
Part₁ ← /×/+≡(⊂⊃(/↥=2)(/↥=3)⊕⧻⊛.⍆°□) Parse
Part₂ ← °□⊢▽:≡(□⟜(=1-∩⧻)▽⊃(=0°□/-)(.°□⊢))⧅< 2 Parse
┌─╴test
  ⍤⤙≍ 12 Part₁ $ abcdef
               $ bababc
               $ abbcde
               $ abcccd
               $ aabcdd
               $ abcdee
               $ ababab
  ⍤⤙≍ "fgij" Part₂ $ abcde
                   $ fghij
                   $ klmno
                   $ pqrst
                   $ fguij
                   $ axcye
                   $ wvxyz
└─╴

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
$"Part 2 returned _ after _ sec":⍜now Part₂ Input
