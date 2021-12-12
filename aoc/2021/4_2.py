# ## --- Part Two ---
#
# On the other hand, it might be wise to try a different strategy: let
# the giant squid win.
#
# You aren't sure how many bingo boards a giant squid could play at
# once, so rather than waste time counting its arms, the safe thing to
# do is to *figure out which board will win last* and choose that one.
# That way, no matter which boards it picks, it will win for sure.
#
# In the above example, the second board is the last to win, which
# happens after `13` is eventually called and its middle column is
# completely marked. If you were to keep playing until this point, the
# second board would have a sum of unmarked numbers equal to `148` for a
# final score of `148 * 13 = *1924*`.
#
# Figure out which board will win last. *Once it wins, what would its
# final score be?*


def mark(board, n):
    for l in board:
        for c in range(5):
            if l[c][0] == n:
                l[c] = n, True


def has_bingo(board):
    for i in range(5):
        if all([board[i][c][1] for c in range(5)]):
            return True
        if all([board[l][i][1] for l in range(5)]):
            return True
    return False


def calc_score(board, last_number):
    unmarked_sum = 0
    for l in board:
        for c in l:
            if not c[1]:
                unmarked_sum += c[0]
    return unmarked_sum * last_number


def evaluate_board(board, numbers):
    for i, n in enumerate(numbers):
        mark(board, n)
        if has_bingo(board):
            return i, calc_score(board, n)

    return 1000, 0


def solve(inp):
    numbers = [int(n) for n in inp.readline().split(",")]
    inp.readline()
    lose_count, score = 0, 0

    board = []
    for line in inp.readlines():
        if line.strip() == "":
            new_count, new_score = evaluate_board(board, numbers)
            if new_count > lose_count:
                lose_count, score = new_count, new_score
            board = []
        else:
            board.append([(int(n), False) for n in line.strip().split()])

    print(lose_count, score)
    return score
