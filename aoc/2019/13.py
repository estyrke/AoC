from io import TextIOWrapper
import math
import functools
import itertools
from .intcode import Machine
import turtle

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = None

    m = Machine.from_stream(inp)

    n = 0
    while not m.halted:
        out = m.run()
        args = [iter(out)] * 3
        for x, y, tile in itertools.zip_longest(*args):
            if tile == 2:
                n += 1
    return n


part2_test_input = part1_test_input

part2_test_output = None

import tcod
import os

TILE_MAP = {0: " ", 1: "X", 2: "#", 3: "-", 4: "o"}


def part2(inp: TextIOWrapper):
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        os.path.join(os.path.dirname(__file__), "dejavu10x10_gs_tc.png"),
        32,
        8,
        tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(42, 26, order="F")
    m = Machine.from_stream(inp)
    m.memory[0] = 2

    game_mode = "AI"
    # game_mode = "Manual"
    # Create a window based on this console and tileset.
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
    ) as context:
        joy_pos = 0
        score = 0
        console.clear()
        last_tick = 0
        paddle_pos = ball_pos = 0

        frame_delay = 0 if game_mode == "AI" else 0.5
        while not m.halted:  # Main loop, runs until SystemExit is raised.
            elapsed = tcod.sys_elapsed_seconds()
            if elapsed > last_tick + frame_delay:
                last_tick = elapsed
                if game_mode == "AI":
                    # Override input
                    if paddle_pos < ball_pos:
                        joy_pos = 1
                    elif paddle_pos > ball_pos:
                        joy_pos = -1
                    else:
                        joy_pos = 0
                out = m.run([joy_pos])

                args = [iter(out)] * 3
                for x, y, tile in itertools.zip_longest(*args):
                    if (x, y) == (-1, 0):
                        score = tile
                    else:
                        if tile == 4:
                            ball_pos = x
                        elif tile == 3:
                            paddle_pos = x
                        console.put_char(x, y, ord(TILE_MAP[tile]))

            for event in tcod.event.wait(0):
                context.convert_event(event)  # Sets tile coordinates for mouse events.

                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.scancode == tcod.event.Scancode.LEFT:
                        joy_pos = -1
                    elif event.scancode == tcod.event.Scancode.RIGHT:
                        joy_pos = 1
                elif isinstance(event, tcod.event.KeyUp):
                    if (
                        event.scancode == tcod.event.Scancode.LEFT
                        or event.scancode == tcod.event.Scancode.RIGHT
                    ):
                        joy_pos = 0
                elif not isinstance(event, tcod.event.MouseMotion):
                    print(event)  # Print event names and attributes.
            console.put_char(0, 25, ord("B") + joy_pos)
            console.print(3, 25, str(score))
            context.present(console)  # Show the console.
        # The window will be closed after the above with-block exits.
        return score if score > 0 else None
