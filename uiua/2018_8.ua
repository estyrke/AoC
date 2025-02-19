# Experimental!
TestData ← "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

Parse ← ⊜⋕ ⊸≠" "

# Extract metadata from the input array
# Metadata RemainingInput ? Count Input
Metadata ← ⊃↙↘

# Recursively parse the data headers
# The function passed will be called with the current metadata and child results
# RemainingInput Result ? Input
Header! ← |1.2 (
  :°⊟ ⊃↙₂↘₂ # Pop the header and uncouple it
  # Now the stack contains MetadataCount ChildCount RemainingInput
  ⊙{⍥(Header!^0)} # Recursively parse the children
  # The result from the previous row is a boxed array where the first element is the remaining input and the rest are the child results
  ⊙⊃(°□⊢|⇌↘1) # So we pop off the remaing input and unbox it. Also reverse the child array
  Metadata
  :
  ⊙^0
)

Part₁ ← (
  Parse
  Header!(⊂⊙/◇⊂) # Simply join the current metadata with the child metadatas
  ◌
  /+
)
┌─╴test
  ⍤⤙≍ 138 Part₁ TestData
└─╴

Part₂ ← (
  Parse
  Header!(
    >0⧻,       # Check if there are children
    ⨬(⊙◌       # If there are no children, pop the empty child array
    | /◇⊂⬚0⊏-1 # Else, use the metadata to index the children (1-based, so subtract 1 before selecting)
    )
    /+ # Sum the metadata
  )
  ◌ # Pop the empty header
)

┌─╴test
  ⍤⤙≍ 66 Part₂ TestData
└─╴

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 8

# $"Part 1 returned _ after _ sec":⍜now Part₁ Input
# $"Part 2 returned _ after _ sec":⍜now Part₂ Input
