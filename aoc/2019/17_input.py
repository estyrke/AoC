from io import StringIO
import itertools
from typing import Iterable, Iterator


class Mem:
    def __init__(self, l):
        self.l = l

    def __getitem__(self, i: int):
        try:
            return self.l[i]
        except IndexError:
            return 0

    def __setitem__(self, i: int, v: int):
        try:
            self.l[i] = v
        except IndexError:
            self.l[len(self.l) : i + 1] = itertools.repeat(0, i + 1 - len(self.l))
            self.l[i] = v


mem = Mem(list(map(int, open("aoc/2019/17_input.txt").read().strip().split(","))))

var_4 = 0
var_5 = 1
# @var_9 = mem[571]  # 0
# @main_routine_len = mem[572]  # 0
# @main_routine_chars = mem[573]  # 0
# @input_char = mem[574]  # 0
# @show_video_feed = mem[575]  # 1
show_video_feed = 1
# @scaffolds_visited = mem[374]  # 0
scaffolds_visited = 0
# @dust_collected = mem[438]  # 0
dust_collected = 0
# @var_9 = mem[570]  # 0
# @chunk_value = mem[571]  # 0
chunk_value = 0
# @robot_x = mem[576]  # 38
robot_x = 38
# @robot_y = mem[577]  # 28
robot_y = 28
# @direction = mem[578]  # 0
direction = 0
# @var_33 = mem[1182]  # 24
var_33 = 24
#    0 add var_4, var_5, is_asleep
# is_asleep = 1
is_asleep = 0  # Modified for part 2


def stop():
    raise StopIteration()


def main(input_it: Iterator[int]):
    global chunk_value
    #    4 base 4588
    #    6 add 1182, 0, compressed_board_ptr
    compressed_board_ptr = 1182
    #   10 mul 1, 1533, pvar_2
    decompressed_board_ptr = 1533  # End of predefined data

    # label_2:

    # Decompress board (RLE compressed at 1182, decompressed at 1533)
    while compressed_board_ptr != 1533:
        #   14 mul 1, mem[compressed_board_ptr], chunk_len
        chunk_len = mem[compressed_board_ptr]
        # label_1:
        while chunk_len > 0:
            #   18 jz chunk_len, label_0
            #   21 mul 1, chunk_value, mem[decompressed_board_ptr]
            mem[decompressed_board_ptr] = chunk_value
            #   25 add chunk_len, -1, chunk_len
            chunk_len -= 1
            #   29 add decompressed_board_ptr, 1, decompressed_board_ptr
            decompressed_board_ptr += 1
            #   33 jz 0, label_1
        # label_0:
        #   36 cmpeq chunk_value, 0, chunk_value
        chunk_value = int(chunk_value == 0)
        #   40 add compressed_board_ptr, 1, compressed_board_ptr
        compressed_board_ptr += 1
        #   44 cmpeq compressed_board_ptr, 1533, var_9
        #   48 jz var_9, label_2

    #   51 add 0, 58, mem[bp + 0]
    #   55 jz 0, update_board
    yield from update_board()
    #   58 jz is_asleep, label_4
    if is_asleep != 0:
        #   61 stop
        stop()
    # label_4:
    #   62 mul 333, 1, mem[bp + 1]
    #   66 add 73, 0, mem[bp + 0]
    #   70 jz 0, label_60
    yield from output_str(333)  # "Main:"
    #   73 mul 0, 1, main_routine_len
    main_routine_len = 0
    #   77 mul 1, 0, main_routine_chars
    main_routine_chars = 0
    # label_11:
    while True:
        #   81 inp input_char
        input_char = next(input_it)
        #   83 add 1, main_routine_chars, main_routine_chars
        main_routine_chars += 1
        #   87 cmplt input_char, 65, var_9
        #   91 jnz var_9, label_7
        #   94 cmplt 67, input_char, var_9
        #   98 jnz var_9, label_7
        if input_char >= 65 and input_char <= 67:
            #  101 add input_char, -64, input_char
            input_char -= 64
            #  105 mul input_char, -1, input_char
            input_char = -input_char
            #  109 add main_routine_len, 1, main_routine_len
            main_routine_len += 1
            #  113 cmplt main_routine_len, 11, var_9
            #  117 jz var_9, label_16
            if main_routine_len >= 11:
                # label_16:
                #  165 mul 1, 514, mem[bp + 1]
                #  169 mul 176, 1, mem[bp + 0]
                #  173 jz 0, label_60
                yield from output_str(
                    514
                )  # '\nDefinitions may be at most 20 characters!\n'
                #  176 stop
                stop()
            #  120 add 1182, main_routine_len, mem[127]
            #  124 mul input_char, 1, mem[0]
            mem[1182 + main_routine_len] = input_char
            #  128 inp input_char
            input_char = next(input_it)
            #  130 add 1, main_routine_chars, main_routine_chars
            main_routine_chars += 1
            #  134 cmpeq input_char, 10, var_9
            #  138 jnz var_9, label_9
            if input_char == 10:
                break
            #  141 cmpeq input_char, 44, var_9
            #  145 jz var_9, label_10
            if input_char != 44:
                # label_10:
                #  158 add 477, 0, mem[bp + 1]
                #  162 jnz 1, label_13
                # label_13:
                #  177 add 0, 184, mem[bp + 0]
                #  181 jz 0, label_60
                yield from output_str(477)  # '\nExpected comma or newline but got: '
                #  184 outp input_char
                yield input_char
                #  186 outp 10
                yield 10
                #  188 stop
                stop()
            #  148 jz 0, label_11
        else:
            # label_7:
            #  151 add 340, 0, mem[bp + 1]
            #  155 jz 0, label_13
            # label_13:
            #  177 add 0, 184, mem[bp + 0]
            #  181 jz 0, label_60
            yield from output_str(340)
            #  184 outp input_char
            yield input_char
            #  186 outp 10
            yield 10
            #  188 stop
            stop()

    # label_16:
    #  165 mul 1, 514, mem[bp + 1]

    #  169 mul 176, 1, mem[bp + 0]
    #  173 jz 0, label_60
    #  176 stop
    # label_13:
    #  177 add 0, 184, mem[bp + 0]
    #  181 jz 0, label_60
    #  184 outp input_char
    #  186 outp 10
    #  188 stop
    # label_9:
    #  189 cmplt main_routine_chars, 22, var_9
    #  193 jz var_9, label_16
    if main_routine_chars >= 22:  # goto label_16
        yield from output_str(514)  # '\nDefinitions may be at most 20 characters!\n'
        stop()
    #  196 mul main_routine_len, 1, var_33
    mem[1182] = main_routine_len
    #  200 mul 1, 375, mem[bp + 1]
    #  204 add 0, 211, mem[bp + 0]
    #  208 jz 0, label_60
    yield from output_str(375)  # 'Function A:\n'
    #  211 add 1182, 11, mem[bp + 1]
    #  215 add 0, 222, mem[bp + 0]
    #  219 jnz 1, read_movement_function
    yield from read_movement_function(input_it, 1182 + 11)
    #  222 add 0, 388, mem[bp + 1]
    #  226 add 0, 233, mem[bp + 0]
    #  230 jnz 1, label_60
    yield from output_str(388)  # 'Function B:\n'
    #  233 add 1182, 22, mem[bp + 1]
    #  237 mul 244, 1, mem[bp + 0]
    #  241 jz 0, read_movement_function
    yield from read_movement_function(input_it, 1182 + 22)
    #  244 mul 401, 1, mem[bp + 1]
    #  248 add 255, 0, mem[bp + 0]
    #  252 jz 0, label_60
    yield from output_str(401)  # 'Function C:\n'
    #  255 add 1182, 33, mem[bp + 1]
    #  259 mul 266, 1, mem[bp + 0]
    #  263 jnz 1, read_movement_function
    yield from read_movement_function(input_it, 1182 + 33)
    #  266 mul 1, 414, mem[bp + 1]
    #  270 mul 277, 1, mem[bp + 0]
    #  274 jnz 1, label_60
    yield from output_str(414)  # 'Continuous video feed?\n'
    #  277 inp show_video_feed
    global show_video_feed
    show_video_feed = next(input_it)
    #  279 cmpeq show_video_feed, 89, var_9
    #  283 cmpeq show_video_feed, 121, show_video_feed
    #  287 add show_video_feed, var_9, show_video_feed
    show_video_feed = show_video_feed == ord("Y") or show_video_feed == ord("y")
    # label_24:
    while input_char != 10:
        #  291 inp input_char
        input_char = next(input_it)
        #  293 cmpeq input_char, 10, var_9
        #  297 jz var_9, label_24
    #  300 outp 10
    yield 10
    #  302 add 0, 1182, mem[bp + 1]
    #  306 add 313, 0, mem[bp + 0]
    #  310 jz 0, execute_routine
    yield from execute_routine(1182)
    #  313 jnz show_video_feed, label_26
    if not show_video_feed:
        #  316 add 0, 1, show_video_feed
        show_video_feed = 1
        #  320 add 0, 327, mem[bp + 0]
        #  324 jz 0, update_board
        yield from update_board()
    # label_26:
    #  327 outp dust_collected
    yield dust_collected
    #  329 stop
    stop()


#  330 data 00, 01, 01, 06, 77, 97, 105, 110
#  338 data 58, 10, 33, 10, 69, 120, 112, 101
#  346 data 99, 116, 101, 100, 32, 102, 117, 110
#  354 data 99, 116, 105, 111, 110, 32, 110, 97
#  362 data 109, 101, 32, 98, 117, 116, 32, 103
#  370 data 111, 116, 58, 32, 00, 12, 70, 117
#  378 data 110, 99, 116, 105, 111, 110, 32, 65
#  386 data 58, 10, 12, 70, 117, 110, 99, 116
#  394 data 105, 111, 110, 32, 66, 58, 10, 12
#  402 data 70, 117, 110, 99, 116, 105, 111, 110
#  410 data 32, 67, 58, 10, 23, 67, 111, 110
#  418 data 116, 105, 110, 117, 111, 117, 115, 32
#  426 data 118, 105, 100, 101, 111, 32, 102, 101
#  434 data 101, 100, 63, 10, 00, 37, 10, 69
#  442 data 120, 112, 101, 99, 116, 101, 100, 32
#  450 data 82, 44, 32, 76, 44, 32, 111, 114
#  458 data 32, 100, 105, 115, 116, 97, 110, 99
#  466 data 101, 32, 98, 117, 116, 32, 103, 111
#  474 data 116, 58, 32, 36, 10, 69, 120, 112
#  482 data 101, 99, 116, 101, 100, 32, 99, 111
#  490 data 109, 109, 97, 32, 111, 114, 32, 110
#  498 data 101, 119, 108, 105, 110, 101, 32, 98
#  506 data 117, 116, 32, 103, 111, 116, 58, 32
#  514 data 43, 10, 68, 101, 102, 105, 110, 105
#  522 data 116, 105, 111, 110, 115, 32, 109, 97
#  530 data 121, 32, 98, 101, 32, 97, 116, 32
#  538 data 109, 111, 115, 116, 32, 50, 48, 32
#  546 data 99, 104, 97, 114, 97, 99, 116, 101
#  554 data 114, 115, 33, 10, 94, 62, 118, 60
#  562 data 00, 01, 00, -1, -1, 00, 01, 00
#  570 data 00, 00, 00, 00, 00, 01, 38, 28
#  578 data  0
# label_60:
def output_str(str_addr):
    #  579 base 4
    #  581 mul 1, mem[bp + -3], mem[586]
    #  585 add mem[0], 0, mem[bp + -1]
    str_len = mem[str_addr]
    #  589 add 1, mem[bp + -3], mem[bp + -3]
    str_addr += 1
    #  593 add 0, 0, mem[bp + -2]
    str_pos = 0
    # label_29:
    #  597 cmpeq mem[bp + -2], mem[bp + -1], var_9
    #  601 jnz var_9, label_28
    while str_pos != str_len:
        #  604 add mem[bp + -3], mem[bp + -2], mem[609]
        #  608 outp mem[0]
        yield mem[str_addr + str_pos]
        #  610 add mem[bp + -2], 1, mem[bp + -2]
        str_pos += 1
        #  614 jnz 1, label_29
    # label_28:
    #  617 base -4
    #  619 jz 0, mem[bp + 0]


# execute_routine:
def execute_routine(addr):  # mem[bp - 4]
    global robot_x, robot_y
    #  622 base 5
    #  624 mul 1, addr, mem[629]
    #  628 add mem[0], 0, routine_len
    routine_len = mem[addr]  # mem[bp - 2]
    #  632 add 1, addr, addr
    addr += 1
    #  636 mul 0, 1, program_ptr
    routine_ptr = 0  # mem[bp + -3]
    # label_43:
    while routine_ptr != routine_len:
        #  640 cmpeq routine_ptr, routine_len, var_9
        #  644 jnz var_9, label_30
        #  647 add addr, routine_ptr, mem[652]
        #  651 mul mem[0], 1, instr
        instr = mem[addr + routine_ptr]  # mem[bp - 1]
        #  655 cmpeq instr, -4, var_9
        #  659 jnz var_9, label_31
        global direction
        if instr == -4:
            # label_31:
            #  709 add direction, 1, direction
            direction += 1
            #  713 cmpeq direction, 4, var_9
            #  717 jz var_9, label_36
            #  720 add direction, -4, direction
            if direction == 4:
                direction -= 4
            # label_36:
            #  724 mul 731, 1, mem[bp + 0]
            #  728 jnz 1, update_board
            yield from update_board()
            #  731 jz 0, label_41
        #  662 cmpeq instr, -5, var_9
        #  666 jnz var_9, label_32
        elif instr == -5:
            # label_32:
            #  734 add direction, -1, direction
            direction -= 1
            #  738 cmpeq direction, -1, var_9
            #  742 jz var_9, label_39
            #  745 add direction, 4, direction
            if direction == -1:
                direction += 4
            # label_39:
            #  749 add 756, 0, mem[bp + 0]
            #  753 jz 0, update_board
            yield from update_board()
            #  756 jz 0, label_41
        #  669 cmplt instr, 0, var_9
        #  673 jnz var_9, label_33
        elif instr < 0:
            # Sub program
            # label_33:
            #  759 mul instr, -11, mem[bp + 1]
            #  763 add 1182, mem[bp + 1], mem[bp + 1]
            #  767 mul 774, 1, mem[bp + 0]
            #  771 jnz 1, execute_routine
            yield from execute_routine(1182 + instr * -11)
        # label_35:
        else:
            # Movement (a number)
            while instr != 0:
                #  676 jz instr, label_41
                #  679 add direction, 562, mem[684]
                #  683 add mem[0], robot_x, robot_x
                robot_x += mem[direction + 562]
                #  687 add direction, 566, mem[692]
                #  691 add mem[0], robot_y, robot_y
                robot_y += mem[direction + 566]
                #  695 add 702, 0, mem[bp + 0]
                #  699 jz 0, update_board
                yield from update_board()
                #  702 add instr, -1, instr
                instr -= 1
                #  706 jnz 1, label_35

        # label_41:
        #  774 add routine_ptr, 1, routine_ptr
        routine_ptr += 1
        #  778 jz 0, label_43
    # label_30:
    #  781 base -5
    #  783 jz 0, mem[bp + 0]


# update_board:
def update_board():
    global show_video_feed, scaffolds_visited, dust_collected, is_dead
    #  786 base 7
    #  788 jnz show_video_feed, label_44
    if show_video_feed == 0:
        #  791 add 0, robot_x, x_pos
        x_pos = robot_x  # mem[bp + -6]
        #  795 mul robot_y, 1, y_pos
        y_pos = robot_y  # mem[bp + -5]
        #  799 jnz 1, label_50
    else:
        # label_44:
        #  802 add 0, 0, is_dead
        is_dead = 0  # mem[bp - 1]
        #  806 add 0, 0, y_pos
        y_pos = 0
        # label_51:
        #  810 mul 0, 1, x_pos
        x_pos = 0
    # label_50:
    while True:
        #  814 cmpeq x_pos, robot_x, is_robot_pos
        #  818 cmpeq y_pos, robot_y, var_9
        #  822 mul var_9, is_robot_pos, is_robot_pos
        is_robot_pos = y_pos == robot_y and x_pos == robot_x  # mem[bp - 2]
        #  826 mul y_pos, 47, board_ptr
        #  830 add x_pos, board_ptr, board_ptr
        #  834 add 1533, board_ptr, board_ptr
        board_ptr = 1533 + y_pos * 47 + x_pos  # mem[bp + -3]
        #  838 add 0, board_ptr, mem[843]
        #  842 jnz mem[0], nlabel_1
        if mem[board_ptr] == 0:  # Not on scaffold
            #  845 mul is_robot_pos, 42, output_char
            output_char = int(is_robot_pos) * 42  # mem[bp + -4]
            #  849 add 46, output_char, output_char
            output_char += 46
            #  853 jz is_robot_pos, 924
            if is_robot_pos:
                #  856 mul 1, 1, is_dead
                is_dead = 1
            #  860 jnz 1, label_47
        # nlabel_1:
        #  863 jnz is_robot_pos, nlabel_2
        elif not is_robot_pos:
            #  866 mul 35, 1, output_char
            output_char = 35
            #  870 jz 0, label_47
        # nlabel_2:
        else:  # robot and on scaffold
            #  873 add 0, board_ptr, mem[878]
            #  877 cmpeq mem[0], 1, var_9
            #  881 jz var_9, label_48
            if mem[board_ptr] == 1:  # Unvisited
                #  884 add scaffolds_visited, 1, scaffolds_visited
                scaffolds_visited += 1
                #  888 add board_ptr, 0, mem[895]
                #  892 add 2, 0, mem[0]
                mem[board_ptr] = 2  # Mark as visited
                #  896 mul 1, board_ptr, mem[902]
                #  900 add dust_collected, 0, dust_collected
                dust_collected += board_ptr
                #  904 mul x_pos, y_pos, var_9
                #  908 add var_9, scaffolds_visited, var_9
                #  912 add var_9, dust_collected, dust_collected
                dust_collected += x_pos * y_pos + scaffolds_visited
            # label_48:
            #  916 add direction, 558, mem[922]
            #  920 add 0, mem[0], output_char
            output_char = mem[direction + 558]
        # label_47:
        #  924 jz show_video_feed, label_49
        if show_video_feed == 0:
            break
        #  927 outp output_char
        yield output_char
        #  929 add 1, x_pos, x_pos
        x_pos += 1
        #  933 cmpeq x_pos, 47, var_9
        #  937 jz var_9, label_50
        if x_pos != 47:
            continue
        #  940 outp 10
        yield 10
        #  942 add 1, y_pos, y_pos
        y_pos += 1
        #  946 cmpeq y_pos, 65, var_9
        #  950 jz var_9, label_51
        if y_pos != 65:
            # label_51:
            #  810 mul 0, 1, x_pos
            x_pos = 0
            continue
        #  953 outp 10
        yield 10
        #  955 jz is_dead, 974
        if is_dead == 0:
            return
        #  958 stop
        stop()
    # label_49:
    #  959 jz is_dead, 974
    if is_dead == 0:
        return
    #  962 mul 1, 1, show_video_feed
    show_video_feed = 1
    #  966 mul 973, 1, mem[bp + 0]
    #  970 jz 0, update_board
    yield from update_board()
    #  973 stop
    stop()
    #  974 base -7
    #  976 jnz 1, mem[bp + 0]


# read_movement_function:
def read_movement_function(input_it, addr):
    #  979 base 6
    #  981 add 0, 0, routine_len
    routine_len = 0  # mem[bp - 4]
    #  985 mul 0, 1, num_chars
    num_chars = 0  # mem[bp - 3]
    # label_56:
    while True:
        #  989 inp input_char
        input_char = next(input_it)  # mem[bp - 2]
        #  991 add 1, num_chars, num_chars
        num_chars += 1
        #  995 cmpeq input_char, 82, mem[bp + -1]
        #  999 jnz mem[bp + -1], 1030
        if input_char == ord("R"):
            # 1030 mul -4, 1, input_char
            input_char = -4

        # 1002 cmpeq input_char, 76, mem[bp + -1]
        # 1006 jnz mem[bp + -1], 1037
        elif input_char == ord("L"):
            # 1037 mul -5, 1, input_char
            input_char = -5
        # 1009 cmplt input_char, 48, mem[bp + -1]
        # 1013 jnz mem[bp + -1], 1124
        # 1016 cmplt 57, input_char, mem[bp + -1]
        # 1020 jnz mem[bp + -1], 1124
        elif input_char < 48 or input_char >= 57:
            # 1124 add 0, 439, mem[bp + 1]
            # 1128 jnz 1, label_58
            # label_58:
            # 1150 mul 1157, 1, mem[bp + 0]
            # 1154 jnz 1, label_60
            yield from output_str(439)  # '\nExpected R, L, or distance but got: '
            # 1157 outp input_char
            yield input_char
            # 1159 outp 10
            yield 10
            # 1161 stop
            stop()

        # 1023 add input_char, -48, input_char
        else:
            input_char -= 48
        # 1027 jnz 1, label_54
        # 1030 mul -4, 1, input_char
        # 1034 jz 0, label_54
        # 1037 mul -5, 1, input_char
        # label_54:
        # 1041 add routine_len, 1, routine_len
        routine_len += 1
        # 1045 cmplt routine_len, 11, mem[bp + -1]
        # 1049 jz mem[bp + -1], 1138
        if routine_len >= 11:
            # 1138 mul 1, 514, mem[bp + 1]
            # 1142 mul 1149, 1, mem[bp + 0]
            # 1146 jnz 1, label_60
            yield from output_str(
                514
            )  # '\nDefinitions may be at most 20 characters!\n'
            # 1149 stop
            stop()
        # 1052 add addr, routine_len, mem[1059]
        # 1056 add 0, input_char, mem[0]
        mem[addr + routine_len] = input_char
        # label_55:
        while True:
            # 1060 inp input_char
            input_char = next(input_it)
            # 1062 add 1, num_chars, num_chars
            num_chars += 1
            # 1066 cmplt input_char, 48, mem[bp + -1]
            # 1070 jnz mem[bp + -1], 1107
            if input_char < 48:
                break
            # 1073 cmplt 57, input_char, mem[bp + -1]
            # 1077 jnz mem[bp + -1], 1107
            if input_char >= 57:
                break
            # 1080 add input_char, -48, input_char
            input_char -= 48
            # 1084 add addr, routine_len, mem[1090]
            # 1088 mul 10, mem[0], mem[bp + -1]
            # 1092 add input_char, mem[bp + -1], input_char
            input_char += 10 * mem[addr + routine_len]
            # 1096 add addr, routine_len, mem[1103]
            # 1100 mul input_char, 1, mem[0]
            mem[addr + routine_len] = input_char
            # 1104 jnz 1, label_55
        # 1107 cmpeq input_char, 10, mem[bp + -1]
        # 1111 jnz mem[bp + -1], 1162
        if input_char == 10:
            break
        # 1114 cmpeq input_char, 44, mem[bp + -1]
        # 1118 jz mem[bp + -1], 1131
        if input_char != 44:
            # 1131 add 0, 477, mem[bp + 1]
            # 1135 jz 0, label_58
            # label_58:
            # 1150 mul 1157, 1, mem[bp + 0]
            # 1154 jnz 1, label_60
            yield from output_str(477)  # '\nExpected comma or newline but got: '
            # 1157 outp input_char
            yield input_char
            # 1159 outp 10
            yield 10
            # 1161 stop
            stop()

        # 1121 jnz 1, label_56

    # 1124 add 0, 439, mem[bp + 1]
    # 1128 jnz 1, label_58
    # 1131 add 0, 477, mem[bp + 1]
    # 1135 jz 0, label_58
    # 1138 mul 1, 514, mem[bp + 1]
    # 1142 mul 1149, 1, mem[bp + 0]
    # 1146 jnz 1, label_60
    # 1149 stop
    # label_58:
    # 1150 mul 1157, 1, mem[bp + 0]
    # 1154 jnz 1, label_60
    # 1157 outp input_char
    # 1159 outp 10
    # 1161 stop
    # 1162 cmplt num_chars, 22, mem[bp + -1]
    # 1166 jz mem[bp + -1], 1138
    if num_chars >= 22:
        # 1138 mul 1, 514, mem[bp + 1]
        # 1142 mul 1149, 1, mem[bp + 0]
        # 1146 jnz 1, label_60
        output_str(514)  # '\nDefinitions may be at most 20 characters!\n'
        # 1149 stop
        stop()
    # 1169 mul 1, addr, mem[1176]
    # 1173 add 0, routine_len, mem[0]
    mem[addr] = routine_len
    # 1177 base -6
    # 1179 jnz 1, mem[bp + 0]


# 1182 data 24,  9, 38,  1,  7,  1, 38,  1
# 1190 data  7,  1, 38,  1,  7,  1, 38,  1
# 1198 data  7,  1, 38,  1,  7,  1, 38,  1
# 1206 data  7,  1, 38,  1,  7,  1, 38,  1
# 1214 data  7,  1, 46,  1, 46,  1, 46,  1
# 1222 data 46,  9, 46,  1, 18,  9, 19,  1
# 1230 data 18,  1,  7,  1, 19,  1, 18,  1
# 1238 data  7,  1, 19,  1, 18,  1,  7,  1
# 1246 data 19,  1, 18,  1,  7,  1, 19,  1
# 1254 data 18,  1,  7,  1, 19,  1, 14,  9
# 1262 data  3,  1,  7, 13, 14,  1,  3,  1
# 1270 data  3,  1,  3,  1,  7,  1, 18, 13
# 1278 data  3,  1,  3,  1,  7,  1, 18,  1
# 1286 data  7,  1,  7,  1,  3,  1,  7,  1
# 1294 data 18,  1,  7,  1,  7,  1,  3,  1
# 1302 data  7,  1, 18,  1,  7,  1,  7,  1
# 1310 data  3,  1,  7,  1, 18,  1,  7,  1
# 1318 data  7,  1,  3, 13, 14,  1,  7,  1
# 1326 data  7,  1, 11,  1,  3,  1, 14,  1
# 1334 data  7,  1,  7,  1,  9, 13,  8,  1
# 1342 data  7,  1,  7,  1,  9,  1,  1,  1
# 1350 data  3,  1, 14,  9,  7,  1,  9,  1
# 1358 data  1,  1,  3,  1, 30,  1,  9,  1
# 1366 data  1,  1,  3,  1, 30, 13,  3,  1
# 1374 data 40,  1,  5,  1, 40,  1,  5,  1
# 1382 data 40,  1,  5,  1, 40,  1,  5,  1
# 1390 data 40,  1,  5,  1, 34, 13, 34,  1
# 1398 data  5,  1, 34, 13, 34,  1,  5,  1
# 1406 data 40,  1,  5,  1, 40,  1,  5,  1
# 1414 data 40,  1,  5,  1, 40,  1,  5,  1
# 1422 data 40,  1,  5, 11, 30,  1, 15,  1
# 1430 data 30,  1, 15,  1,  7,  9, 14,  1
# 1438 data 15,  1,  7,  1,  7,  1, 14,  1
# 1446 data 15,  1,  7,  1,  7,  1, 14,  1
# 1454 data 15,  1,  7,  1,  7,  1, 14, 13
# 1462 data  3,  1,  7,  1,  7,  1, 26,  1
# 1470 data  3,  1,  7,  1,  7,  1, 26,  1
# 1478 data  3,  1,  7,  1,  7,  1, 26,  1
# 1486 data  3,  1,  7,  1,  7,  1, 26,  1
# 1494 data  3,  1,  3, 13, 26,  1,  3,  1
# 1502 data  3,  1,  3,  1, 34,  1,  3,  9
# 1510 data 34,  1,  7,  1, 38,  1,  7,  1
# 1518 data 38,  1,  7,  1, 38,  1,  7,  1
# 1526 data 38,  1,  7,  1, 38,  9, 12

if __name__ == "__main__":

    A = "L,12,L,12,R,12\n"
    B = "L,8,L,8,R,12,L,8,L,8\n"
    C = "L,10,R,8,R,12\n"
    MAIN = "A,A,B,C,C,A,B,C,A,B\n"

    b = StringIO()
    answer = None
    prev = None
    for x in main(map(ord, MAIN + A + B + C + "y\n")):
        if x > 255:
            answer = x
            break

        if prev == x == 10:
            print(b.getvalue()[:-1], end="")
            b = StringIO()
        else:
            b.write(chr(x))

        prev = x

    print(answer)
