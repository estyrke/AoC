from io import StringIO, TextIOWrapper
import sys

part1_test_input = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

part1_test_output = 5


def part1(inp: TextIOWrapper):
    lines = [l.strip().split("~") for l in inp.readlines()]
    blocks = [
        tuple(tuple(int(c) for c in p.split(",")) for p in line) for line in lines
    ]

    max_x: int = max([max(x1, x2) for (x1, y1, z1), (x2, y2, z2) in blocks])
    max_y: int = max([max(y1, y2) for (x1, y1, z1), (x2, y2, z2) in blocks])
    blocks = sorted(
        blocks, key=lambda b: (min(b[0][2], b[1][2]), max(b[0][2], b[1][2]))
    )
    contour: list[list[tuple[int, int]]] = [
        [(-1, 0) for _ in range(max_x + 1)] for _ in range(max_y + 1)
    ]
    stable = set()
    unstable = set()
    free_top = set(range(len(blocks)))
    for block_id, block in enumerate(blocks):
        (x1, y1, z1), (x2, y2, z2) = block
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))
        max_h = 0

        resting_blocks = set()
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                resting, h = contour[y][x]
                assert h < z1
                if h > max_h:
                    # Found a higher resting point, clear the current list of resting blocks
                    max_h = h
                    resting_blocks = set([resting])
                elif h == max_h:
                    # Found an equal resting point, add to the current list of resting blocks
                    resting_blocks.add(resting)

        for r in resting_blocks:
            # any blocks supporting this one are not free upwards anymore
            if r >= 0:
                if r in free_top:
                    free_top.remove(r)
        if len(resting_blocks) > 1:
            # If this block is supported by two or more blocks, those are candidates for disintegration
            assert -1 not in resting_blocks
            stable |= resting_blocks
        elif len(resting_blocks) == 1:
            # If this block is supported by only one block, that block must not be disintegrated
            if -1 not in resting_blocks:
                unstable |= resting_blocks

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                contour[y][x] = (block_id, max_h + z2 - z1 + 1)

    # The answer is the set of stable blocks unless they also are the sole support of some other block.
    # Add to that the blocks that do not support any other block at all
    answer = len((stable - unstable) | free_top)
    return answer


part2_test_input = part1_test_input

part2_test_output = 7


def part2(inp: TextIOWrapper):
    lines = [l.strip().split("~") for l in inp.readlines()]
    blocks = [
        tuple(tuple(int(c) for c in p.split(",")) for p in line) for line in lines
    ]

    max_x: int = max([max(x1, x2) for (x1, y1, z1), (x2, y2, z2) in blocks])
    max_y: int = max([max(y1, y2) for (x1, y1, z1), (x2, y2, z2) in blocks])
    blocks = sorted(
        blocks, key=lambda b: (min(b[0][2], b[1][2]), max(b[0][2], b[1][2]))
    )
    contour: list[list[tuple[int, int]]] = [
        [(-1, 0) for _ in range(max_x + 1)] for _ in range(max_y + 1)
    ]
    on_top: dict[int, set[int]] = {id: set() for id in range(len(blocks))}
    below: dict[int, set[int]] = {id: set() for id in range(len(blocks))}
    for block_id, block in enumerate(blocks):
        (x1, y1, z1), (x2, y2, z2) = block
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))
        max_h = 0

        resting_blocks = set()
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                resting, h = contour[y][x]
                assert h < z1
                if h > max_h:
                    # Found a higher resting point, clear the current list of resting blocks
                    max_h = h
                    resting_blocks = set([resting])
                elif h == max_h:
                    # Found an equal resting point, add to the current list of resting blocks
                    resting_blocks.add(resting)

        # Update relationships
        for r in resting_blocks:
            if r >= 0:
                assert r in on_top
                on_top[r].add(block_id)
                below[block_id].add(r)

        # Update contour map
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                contour[y][x] = (block_id, max_h + z2 - z1 + 1)

    # For each block, disintegrate it and all blocks above it
    # that does not also rest on a non-disintegrated block.
    answer = 0
    for block_id in range(len(blocks)):
        disintegrated = set([block_id])
        queue = [block_id]
        while queue:
            b = queue.pop(0)
            for ot in on_top[b]:
                if len(below[ot] - disintegrated) == 0:
                    disintegrated.add(ot)
                    queue.append(ot)
        answer += len(disintegrated) - 1
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
