$ initial state: #..#.#..##......###...###
$ 
$ ...## => #
$ ..#.. => #
$ .#... => #
$ .#.#. => #
$ .#.## => #
$ .##.. => #
$ .#### => #
$ #.#.# => #
$ #.### => #
$ ##.#. => #
$ ##.## => #
$ ###.. => #
$ ###.# => #
$ ####. => #
TestInput ←

Parse ← (
  °$"initial state: _\n\n_"
  :
  ⊜({°$"_ => _"?}) ⊸≠@\n
)

Part₁ ← (
  Parse
  ?
)

┌─╴test
  ⍤⤙≍ 325 Part₁ TestInput
└─╴

Part₂ ← (
  Parse
  Solve
)

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 10

$"Part 1 returned after _ sec" ⊙◌ ⍜now Part₁ Input
$"Part 2 returned _" ⤙⊙◌
