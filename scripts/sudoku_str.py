#!/usr/bin/env python

# SudokuStr() can take three kinds of input:
# An 81 character str
s = '......2.38.52.......31..4....2..1....586.231.3..9..6....4..85.......39.89.1......'

# Or a multiline str
s = '''......2.3
       8.52.....
       ..31..4..
       ..2..1...
       .586.231.
       3..9..6..
       ..4..85..
       .....39.8
       9.1......'''

# Or a list or tuple
s = [[' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', '3'],
     ['8', ' ', '5', '2', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', '3', '1', ' ', ' ', '4', ' ', ' '],
     [' ', ' ', '2', ' ', ' ', '1', ' ', ' ', ' '],
     [' ', '5', '8', '6', ' ', '2', '3', '1', ' '],
     ['3', ' ', ' ', '9', ' ', ' ', '6', ' ', ' '],
     [' ', ' ', '4', ' ', ' ', '8', '5', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', '3', '9', ' ', '8'],
     ['9', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ']]


class SudokuStr(object):
    def __init__(self, s=s):
        if isinstance(s, str):
            self.s = ''.join(line.lstrip() for line in s.splitlines())
        elif isinstance(s, (list, tuple)):
            if len(s) == 9:
                self.s = ''.join(''.join(row for row in col) for col in s)
            elif len(s) == 81:
                self.s = ''.join(s)
        assert len(self.s) == 9 * 9, 'A SudokuStr must be 81 characters long'
        self.s = self.s.replace(' ', '.').replace('0', '.').replace('_', '.')

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.s)

    def __str__(self):
        return self.sudoku_board()
    
    @classmethod
    def border_line(cls):
        return ('=' * 7).join('+' * 4)

    @classmethod
    def get_fmt(cls, i):
        return '{}' if i % 3 else '+ {}'

    @classmethod
    def sudoku_line(cls, i, line):
        s = '' if i % 3 else cls.border_line() + '\n'
        return s + ' '.join(cls.get_fmt(i).format(x if x != '0' else '_')
            for i, x in enumerate(line)) + ' +'

    def board_rows(self):
        for i in range(9):
            yield self.s[i*9:(i+1)*9]

    def sudoku_board(self):
        return '\n'.join(self.sudoku_line(i, line) for i, line
            in enumerate(self.board_rows())) + '\n' + self.border_line()

if __name__ == '__main__:
    print(repr(SudokuStr()))
    print(SudokuStr())
