#!/usr/bin/env python
# coding: utf-8

import sudopy  # see: http://norvig.com/sudopy.shtml

"""
SudokuStr(sudoku) can take three kinds of input:
* An 81 character str
* Or a multiline str
* Or a list or tuple
"""

# An 81 character str
s0 = '......2.38.52.......31..4....2..1....586.231.3..9..6....4..85.......39.89.1......'
s0 = '      2 38 52       31  4    2  1    586 231 3  9  6    4  85       39 89 1      '


# Or a multiline str
s1 = '''......2.3
        8.52.....
        ..31..4..
        ..2..1...
        .586.231.
        3..9..6..
        ..4..85..
        .....39.8
        9.1......'''

# Or a list or tuple
s2 = [[' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', '3'],
      ['8', ' ', '5', '2', ' ', ' ', ' ', ' ', ' '],
      [' ', ' ', '3', '1', ' ', ' ', '4', ' ', ' '],
      [' ', ' ', '2', ' ', ' ', '1', ' ', ' ', ' '],
      [' ', '5', '8', '6', ' ', '2', '3', '1', ' '],
      ['3', ' ', ' ', '9', ' ', ' ', '6', ' ', ' '],
      [' ', ' ', '4', ' ', ' ', '8', '5', ' ', ' '],
      [' ', ' ', ' ', ' ', ' ', '3', '9', ' ', '8'],
      ['9', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ']]


class SudokuStr(object):
    def __init__(self, sudoku=s0):
        self.s = self.sudoku_to_str(sudoku)

    @staticmethod
    def sudoku_to_str(sudoku):
        s = ''
        if isinstance(sudoku, str):
            if '\n' in sudoku:  # a multiline string
                s = ''.join(line.lstrip() for line in sudoku.splitlines())
            else:               # a single line string
                s = sudoku
        elif isinstance(sudoku, (list, tuple)):
            if len(sudoku) == 9:
                s = ''.join(''.join(row for row in col) for col in sudoku)
            elif len(sudoku) == 81:
                s = ''.join(sudoku)
        assert len(s) == 9 * 9, 'A SudokuStr must be 81 characters long'
        return s.replace(' ', '.').replace('0', '.').replace('_', '.')

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.s)

    def __str__(self):
        return self.sudoku_board()

    @staticmethod
    def border_line():
        return ('-' * 7).join('|' * 4)

    @staticmethod
    def get_fmt(i):
        return '{}' if i % 3 else '| {}'

    @classmethod
    def sudoku_line(cls, i, line):
        s = '' if i % 3 else cls.border_line() + '\n'
        return s + ' '.join(cls.get_fmt(i).format(x if x != '0' else '_')
            for i, x in enumerate(line)) + ' |'

    def board_rows(self):
        for i in range(9):
            yield self.s[i*9:(i+1)*9]

    def sudoku_board(self):
        return '\n'.join(self.sudoku_line(i, line) for i, line
            in enumerate(self.board_rows())) + '\n' + self.border_line()

    def solve(self):
        if not sudopy.parse_grid(self.s):
            raise ValueError('Sudoku puzzle is not solvable.\n> ' + self.s)
        self.s = ''.join(sudopy.solve(self.s))
        return self  # enables: print(s.solve())

if __name__ == '__main__':
    s = SudokuStr()
    assert s.s == SudokuStr(s1).s, 'Multiline str failure'
    assert s.s == SudokuStr(s2).s, 'List failure'
    assert s.s == SudokuStr(tuple(s2)).s, 'Tuple failure'
    print(repr(s))
    print(s)
    try:
        print('\nSolving...\n\n{}'.format(s.solve()))
    except ValueError:
        print('No solution found.  Please rescan the puzzle.')
