@var_1 = mem[330]  # 0
@var_2 = mem[331]  # 1
@var_3 = mem[332]  # 1
@var_4 = mem[570]  # 0
@var_5 = mem[571]  # 0
@var_6 = mem[572]  # 0
@var_7 = mem[573]  # 0
@var_8 = mem[574]  # 0
@var_9 = mem[1182]  # 24
@var_10 = mem[575]  # 1
@var_11 = mem[438]  # 0
@var_12 = mem[578]  # 0
@var_13 = mem[576]  # 38
@var_14 = mem[577]  # 28
@var_15 = mem[374]  # 0
    0 mul var_1, var_2, var_3
    4 base 4588
    6 add 1182, 0, pvar_1
   10 mul 1, 1533, pvar_2
label_3:
   14 mul 1, mem[pvar_1], var_4
label_2:
   18 jz var_4, label_1
   21 mul 1, var_5, mem[pvar_2]
   25 add var_4, -1, var_4
   29 add pvar_2, 1, pvar_2
   33 jz 0, label_2
label_1:
   36 cmpeq var_5, 0, var_5
   40 add pvar_1, 1, pvar_1
   44 cmpeq pvar_1, 1533, var_4
   48 jz var_4, label_3
   51 add 0, 58, mem[bp + 0]
   55 jz 0, label_4
   58 jz var_3, label_5
   61 stop
label_5:
   62 mul 333, 1, mem[bp + 1]
   66 add 73, 0, mem[bp + 0]
   70 jz 0, label_6
   73 mul 0, 1, var_6
   77 mul 1, 0, var_7
label_12:
   81 inp var_8
   83 add 1, var_7, var_7
   87 cmplt var_8, 65, var_4
   91 jnz var_4, label_7
   94 cmplt 67, var_8, var_4
   98 jnz var_4, label_7
  101 add var_8, -64, var_8
  105 mul var_8, -1, var_8
  109 add var_6, 1, var_6
  113 cmplt var_6, 11, var_4
  117 jz var_4, label_9
  120 add 1182, var_6, pvar_3
  124 mul var_8, 1, mem[pvar_3]
  128 inp var_8
  130 add 1, var_7, var_7
  134 cmpeq var_8, 10, var_4
  138 jnz var_4, label_10
  141 cmpeq var_8, 44, var_4
  145 jz var_4, label_11
  148 jz 0, label_12
label_7:
  151 add 340, 0, mem[bp + 1]
  155 jz 0, label_13
label_11:
  158 add 477, 0, mem[bp + 1]
  162 jnz 1, label_13
label_9:
  165 mul 1, 514, mem[bp + 1]
  169 mul 176, 1, mem[bp + 0]
  173 jz 0, label_6
  176 stop
label_13:
  177 add 0, 184, mem[bp + 0]
  181 jz 0, label_6
  184 outp var_8
  186 outp 10
  188 stop
label_10:
  189 cmplt var_7, 22, var_4
  193 jz var_4, label_9
  196 mul var_6, 1, var_9
  200 mul 1, 375, mem[bp + 1]
  204 add 0, 211, mem[bp + 0]
  208 jz 0, label_6
  211 add 1182, 11, mem[bp + 1]
  215 add 0, 222, mem[bp + 0]
  219 jnz 1, label_19
  222 add 0, 388, mem[bp + 1]
  226 add 0, 233, mem[bp + 0]
  230 jnz 1, label_6
  233 add 1182, 22, mem[bp + 1]
  237 mul 244, 1, mem[bp + 0]
  241 jz 0, label_19
  244 mul 401, 1, mem[bp + 1]
  248 add 255, 0, mem[bp + 0]
  252 jz 0, label_6
  255 add 1182, 33, mem[bp + 1]
  259 mul 266, 1, mem[bp + 0]
  263 jnz 1, label_19
  266 mul 1, 414, mem[bp + 1]
  270 mul 277, 1, mem[bp + 0]
  274 jnz 1, label_6
  277 inp var_10
  279 cmpeq var_10, 89, var_4
  283 cmpeq var_10, 121, var_10
  287 add var_10, var_4, var_10
label_25:
  291 inp var_8
  293 cmpeq var_8, 10, var_4
  297 jz var_4, label_25
  300 outp 10
  302 add 0, 1182, mem[bp + 1]
  306 add 313, 0, mem[bp + 0]
  310 jz 0, label_26
  313 jnz var_10, label_27
  316 add 0, 1, var_10
  320 add 0, 327, mem[bp + 0]
  324 jz 0, label_4
label_27:
  327 outp var_11
  329 stop
  330 data 0, 1, 1, 6, 77, 97, 105, 110, 58, 10, 33, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 110, 97, 109, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 0, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 65, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 66, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 67, 58, 10, 23, 67, 111, 110, 116, 105, 110, 117, 111, 117, 115, 32, 118, 105, 100, 101, 111, 32, 102, 101, 101, 100, 63, 10, 0, 37, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 82, 44, 32, 76, 44, 32, 111, 114, 32, 100, 105, 115, 116, 97, 110, 99, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 36, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 99, 111, 109, 109, 97, 32, 111, 114, 32, 110, 101, 119, 108, 105, 110, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 43, 10, 68, 101, 102, 105, 110, 105, 116, 105, 111, 110, 115, 32, 109, 97, 121, 32, 98, 101, 32, 97, 116, 32, 109, 111, 115, 116, 32, 50, 48, 32, 99, 104, 97, 114, 97, 99, 116, 101, 114, 115, 33, 10, 94, 62, 118, 60, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 38, 28, 0
label_6:
@lvar_3 = mem[bp + -3]
@lvar_1 = mem[bp + -1]
@lvar_2 = mem[bp + -2]
  579 base 4
  581 mul 1, lvar_3, pvar_4
  585 add mem[pvar_4], 0, lvar_1
  589 add 1, lvar_3, lvar_3
  593 add 0, 0, lvar_2
label_58:
  597 cmpeq lvar_2, lvar_1, var_4
  601 jnz var_4, label_57
  604 add lvar_3, lvar_2, pvar_5
  608 outp mem[pvar_5]
  610 add lvar_2, 1, lvar_2
  614 jnz 1, label_58
label_57:
  617 base -4
  619 jz 0, mem[bp + 0]
label_26:
@lvar_4 = mem[bp + -4]
@lvar_2 = mem[bp + -2]
@lvar_3 = mem[bp + -3]
@lvar_1 = mem[bp + -1]
  622 base 5
  624 mul 1, lvar_4, pvar_6
  628 add mem[pvar_6], 0, lvar_2
  632 add 1, lvar_4, lvar_4
  636 mul 0, 1, lvar_3
label_73:
  640 cmpeq lvar_3, lvar_2, var_4
  644 jnz var_4, label_59
  647 add lvar_4, lvar_3, pvar_7
  651 mul mem[pvar_7], 1, lvar_1
  655 cmpeq lvar_1, -4, var_4
  659 jnz var_4, label_60
  662 cmpeq lvar_1, -5, var_4
  666 jnz var_4, label_61
  669 cmplt lvar_1, 0, var_4
  673 jnz var_4, label_62
label_65:
  676 jz lvar_1, label_63
  679 add var_12, 562, pvar_8
  683 add mem[pvar_8], var_13, var_13
  687 add var_12, 566, pvar_9
  691 add mem[pvar_9], var_14, var_14
  695 add 702, 0, mem[bp + 0]
  699 jz 0, label_4
  702 add lvar_1, -1, lvar_1
  706 jnz 1, label_65
label_60:
  709 add var_12, 1, var_12
  713 cmpeq var_12, 4, var_4
  717 jz var_4, label_66
  720 add var_12, -4, var_12
label_66:
  724 mul 731, 1, mem[bp + 0]
  728 jnz 1, label_4
  731 jz 0, label_63
label_61:
  734 add var_12, -1, var_12
  738 cmpeq var_12, -1, var_4
  742 jz var_4, label_69
  745 add var_12, 4, var_12
label_69:
  749 add 756, 0, mem[bp + 0]
  753 jz 0, label_4
  756 jz 0, label_63
label_62:
  759 mul lvar_1, -11, mem[bp + 1]
  763 add 1182, mem[bp + 1], mem[bp + 1]
  767 mul 774, 1, mem[bp + 0]
  771 jnz 1, label_26
label_63:
  774 add lvar_3, 1, lvar_3
  778 jz 0, label_73
label_59:
  781 base -5
  783 jz 0, mem[bp + 0]
label_4:
@lvar_6 = mem[bp + -6]
@lvar_5 = mem[bp + -5]
@lvar_1 = mem[bp + -1]
@lvar_2 = mem[bp + -2]
@lvar_3 = mem[bp + -3]
@lvar_4 = mem[bp + -4]
  786 base 7
  788 jnz var_10, label_74
  791 add 0, var_13, lvar_6
  795 mul var_14, 1, lvar_5
  799 jnz 1, label_75
label_74:
  802 add 0, 0, lvar_1
  806 add 0, 0, lvar_5
label_84:
  810 mul 0, 1, lvar_6
label_75:
  814 cmpeq lvar_6, var_13, lvar_2
  818 cmpeq lvar_5, var_14, var_4
  822 mul var_4, lvar_2, lvar_2
  826 mul lvar_5, 47, lvar_3
  830 add lvar_6, lvar_3, lvar_3
  834 add 1533, lvar_3, lvar_3
  838 add 0, lvar_3, pvar_10
  842 jnz mem[pvar_10], label_76
  845 mul lvar_2, 42, lvar_4
  849 add 46, lvar_4, lvar_4
  853 jz lvar_2, label_77
  856 mul 1, 1, lvar_1
  860 jnz 1, label_77
label_76:
  863 jnz lvar_2, label_79
  866 mul 35, 1, lvar_4
  870 jz 0, label_77
label_79:
  873 add 0, lvar_3, pvar_11
  877 cmpeq mem[pvar_11], 1, var_4
  881 jz var_4, label_81
  884 add var_15, 1, var_15
  888 add lvar_3, 0, pvar_12
  892 add 2, 0, mem[pvar_12]
  896 mul 1, lvar_3, pvar_13
  900 add var_11, pvar_13, var_11
  904 mul lvar_6, lvar_5, var_4
  908 add var_4, var_15, var_4
  912 add var_4, var_11, var_11
label_81:
  916 add var_12, 558, pvar_14
  920 add 0, mem[pvar_14], lvar_4
label_77:
  924 jz var_10, label_82
  927 outp lvar_4
  929 add 1, lvar_6, lvar_6
  933 cmpeq lvar_6, 47, var_4
  937 jz var_4, label_75
  940 outp 10
  942 add 1, lvar_5, lvar_5
  946 cmpeq lvar_5, 65, var_4
  950 jz var_4, label_84
  953 outp 10
  955 jz lvar_1, label_85
  958 stop
label_82:
  959 jz lvar_1, label_85
  962 mul 1, 1, var_10
  966 mul 973, 1, mem[bp + 0]
  970 jz 0, label_4
  973 stop
label_85:
  974 base -7
  976 jnz 1, mem[bp + 0]
label_19:
@lvar_4 = mem[bp + -4]
@lvar_3 = mem[bp + -3]
@lvar_2 = mem[bp + -2]
@lvar_1 = mem[bp + -1]
@lvar_5 = mem[bp + -5]
  979 base 6
  981 add 0, 0, lvar_4
  985 mul 0, 1, lvar_3
label_100:
  989 inp lvar_2
  991 add 1, lvar_3, lvar_3
  995 cmpeq lvar_2, 82, lvar_1
  999 jnz lvar_1, label_88
 1002 cmpeq lvar_2, 76, lvar_1
 1006 jnz lvar_1, label_89
 1009 cmplt lvar_2, 48, lvar_1
 1013 jnz lvar_1, label_90
 1016 cmplt 57, lvar_2, lvar_1
 1020 jnz lvar_1, label_90
 1023 add lvar_2, -48, lvar_2
 1027 jnz 1, label_92
label_88:
 1030 mul -4, 1, lvar_2
 1034 jz 0, label_92
label_89:
 1037 mul -5, 1, lvar_2
label_92:
 1041 add lvar_4, 1, lvar_4
 1045 cmplt lvar_4, 11, lvar_1
 1049 jz lvar_1, label_94
 1052 add lvar_5, lvar_4, pvar_15
 1056 add 0, lvar_2, mem[pvar_15]
label_97:
 1060 inp lvar_2
 1062 add 1, lvar_3, lvar_3
 1066 cmplt lvar_2, 48, lvar_1
 1070 jnz lvar_1, label_95
 1073 cmplt 57, lvar_2, lvar_1
 1077 jnz lvar_1, label_95
 1080 add lvar_2, -48, lvar_2
 1084 add lvar_5, lvar_4, pvar_16
 1088 mul 10, mem[pvar_16], lvar_1
 1092 add lvar_2, lvar_1, lvar_2
 1096 add lvar_5, lvar_4, pvar_17
 1100 mul lvar_2, 1, mem[pvar_17]
 1104 jnz 1, label_97
label_95:
 1107 cmpeq lvar_2, 10, lvar_1
 1111 jnz lvar_1, label_98
 1114 cmpeq lvar_2, 44, lvar_1
 1118 jz lvar_1, label_99
 1121 jnz 1, label_100
label_90:
 1124 add 0, 439, mem[bp + 1]
 1128 jnz 1, label_101
label_99:
 1131 add 0, 477, mem[bp + 1]
 1135 jz 0, label_101
label_94:
 1138 mul 1, 514, mem[bp + 1]
 1142 mul 1149, 1, mem[bp + 0]
 1146 jnz 1, label_6
 1149 stop
label_101:
 1150 mul 1157, 1, mem[bp + 0]
 1154 jnz 1, label_6
 1157 outp lvar_2
 1159 outp 10
 1161 stop
label_98:
 1162 cmplt lvar_3, 22, lvar_1
 1166 jz lvar_1, label_94
 1169 mul 1, lvar_5, pvar_18
 1173 add 0, lvar_4, mem[pvar_18]
 1177 base -6
 1179 jnz 1, mem[bp + 0]
 1182 data 24, 9, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 46, 1, 46, 1, 46, 1, 46, 9, 46, 1, 18, 9, 19, 1, 18, 1, 7, 1, 19, 1, 18, 1, 7, 1, 19, 1, 18, 1, 7, 1, 19, 1, 18, 1, 7, 1, 19, 1, 18, 1, 7, 1, 19, 1, 14, 9, 3, 1, 7, 13, 14, 1, 3, 1, 3, 1, 3, 1, 7, 1, 18, 13, 3, 1, 3, 1, 7, 1, 18, 1, 7, 1, 7, 1, 3, 1, 7, 1, 18, 1, 7, 1, 7, 1, 3, 1, 7, 1, 18, 1, 7, 1, 7, 1, 3, 1, 7, 1, 18, 1, 7, 1, 7, 1, 3, 13, 14, 1, 7, 1, 7, 1, 11, 1, 3, 1, 14, 1, 7, 1, 7, 1, 9, 13, 8, 1, 7, 1, 7, 1, 9, 1, 1, 1, 3, 1, 14, 9, 7, 1, 9, 1, 1, 1, 3, 1, 30, 1, 9, 1, 1, 1, 3, 1, 30, 13, 3, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 34, 13, 34, 1, 5, 1, 34, 13, 34, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 1, 40, 1, 5, 11, 30, 1, 15, 1, 30, 1, 15, 1, 7, 9, 14, 1, 15, 1, 7, 1, 7, 1, 14, 1, 15, 1, 7, 1, 7, 1, 14, 1, 15, 1, 7, 1, 7, 1, 14, 13, 3, 1, 7, 1, 7, 1, 26, 1, 3, 1, 7, 1, 7, 1, 26, 1, 3, 1, 7, 1, 7, 1, 26, 1, 3, 1, 7, 1, 7, 1, 26, 1, 3, 1, 3, 13, 26, 1, 3, 1, 3, 1, 3, 1, 34, 1, 3, 9, 34, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 1, 7, 1, 38, 9, 12
