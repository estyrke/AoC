$ Step C must be finished before step A can begin.
$ Step C must be finished before step F can begin.
$ Step A must be finished before step B can begin.
$ Step A must be finished before step D can begin.
$ Step B must be finished before step E can begin.
$ Step D must be finished before step E can begin.
$ Step F must be finished before step E can begin.
TestInput ←

Parse ← (
  ⊸≠@\n                                                    # Split by newline
  ⊜(⊂°$"Step _ must be finished before step _ can begin.") # Parse input
)

InDegree  ← /+
OutDegree ← ⍜⍉/+

┌─╴State
  New         ← {⊙⊙⊙¯1}
  Result      ← °□⊡0
  Queue       ← °□⊡1
  Adj         ← °□⊡2
  Current     ← °□⊡3
  CurrentSucc ← ⊏ ⊃Current Adj
└─╴

Part₁ ← (
  Parse
  °⊚ -@A # Get an adjacency matrix
  ⊚=0⊸InDegree
  []
  State
  ⍢(⍜State~Queue(⊃↘₁⊢⍆) # Pop the top element of the queue
    ⊸⍜State~Result(⊂)   # Push the first element of the queue to the result
    ⍜State~Current(◌)   # Put the top element as current
    ⊸State~CurrentSucc  # Get the successors of the current element
    :
    ⍜⊏(↥0-1) ⊸⊃State~Current State~Adj # Extract the adjacency matrix and decrement the in-degree of the successors
    ⍜State~Adj(◌):                     # Put the adjacency matrix back
    InDegree ⊸State~Adj                # Get the in-degrees of all elements
    ⍜State~Queue(⊂⊙(⊚×=0)) :           # Push the successors to the queue if they have in-degree 0
  | >0⧻⊸State~Queue                    # While the queue is not empty
  )
  +@A State~Result # Extract the result and convert it to a string
)

┌─╴test
  ⍤⤙≍ "CABDFE" Part₁ TestInput
└─╴

┌─╴State₂
  New         ← {⊙⊙⊙⊙⊙∘}
  Result      ← °□⊡0
  Queue       ← °□⊡1
  Adj         ← °□⊡2
  Current     ← °□⊡3
  Workers     ← °□⊡4
  BaseCost    ← °□⊡5
  CurrentSucc ← ⊏ ⊃Current Adj
└─╴

Part₂ ← (
  ⊙⊙$BaseCost
  ⊙($Workers ⊚)
  Parse
  $Adj °⊚ -@A # Get an adjacency matrix
  $Queue≡⊟0⊚=0⊸InDegree
  $Result[]
  ⊙⊙⊙($Current ¯1)
  State₂
  ⍢(⍜State₂~Queue(⊃↘₁($Current ⊢)⍆) # Pop the top element of the queue
    ⟜State₂~BaseCost                # Get the base cost
    ⍜State₂~Workers(
      ⊙($WorkerBusyFor ++1⊣,) # Worker will be busy for BaseCost + current index + 1
      ⍜⊢(
        ⊃(↥⊙⋅⊸⊢|⋅∘)                # The start time is the minimum of the worker's first free time and the time the current element finishes
        ⊃($WorkerBusyUntil+⊙⋅∘|⋅∘) # The end time is the start time plus $WorkerBusyFor
      ) ⍆
    ) # Update the workers. If the queue is empty, no worker can continue before this item is done.
    # ⍜State₂~Result (?⊂?⊙(□$⊂?,)) # Push the first element of the queue to the result
    ⍜State₂~Result(⊂□$,)
    ⍜State₂~Current($Current⊣◌) # Put the top element as current
    ⊸State₂~CurrentSucc         # Get the successors of the current element
    :
    ⍜⊏(↥0-1) ⊸⊃State₂~Current State₂~Adj # Extract the adjacency matrix and decrement the in-degree of the successors
    ⍜State₂~Adj(◌):                      # Put the adjacency matrix back
    InDegree ⊸State₂~Adj                 # Get the in-degrees of all elements
    : ⊙(⊚×=0) :
    ⊙(⊢⊸State₂~Workers)
    ≡(⊟:)             # Couple each successor with the done-time of the current worker
    ⍜State₂~Queue(⊂): # Push the successors to the queue if they have in-degree 0
  | >0⧻⊸State₂~Queue  # While the queue is not empty
  )
  ⊃State₂~Result State₂~BaseCost
  ≡(+1+/+°□) # Add the final item's time to each result
  /↥
)

┌─╴test
  ⍤⤙≍ 15 Part₂ TestInput 2 0
└─╴

~ "git: github.com/amatgil/steal-gift" ~ AoCGet
Input ← AoCGet 2018 7

$"Part 1 returned _ after _ sec":⍜now Part₁ Input
$"Part 2 returned _ after _ sec":⍜now Part₂ Input 5 60
