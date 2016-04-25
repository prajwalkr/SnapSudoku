from __future__ import print_function  # prepare for Python 3
import numpy as np
import cv2

from helpers import Helpers
from digit import Digit


class Cells(object):
    '''
    Extracts each cell from the sudoku grid obtained
    from the Extractor
    '''

    def __init__(self, sudoku):
        print('Extracting cells...', end='')
        self.helpers = Helpers()
        self.cells = self.extractCells(sudoku)
        print('done.')

    def extractCells(self, sudoku):
        cells = []
        W, H = sudoku.shape
        cell_size = W / 9
        i, j = 0, 0
        for r in range(0, W, cell_size):
            row = []
            j = 0
            for c in range(0, W, cell_size):
                cell = sudoku[r:r + cell_size, c:c + cell_size]
                cell = self.helpers.make_it_square(cell, 28)
                #self.helpers.show(cell, 'Before clean')
                cell = self.clean(cell)
                digit = Digit(cell).digit
                #self.helpers.show(digit, 'After clean')
                digit = self.centerDigit(digit)
                #self.helpers.show(digit, 'After centering')
                row.append(digit // 255)
                j += 1
            cells.append(row)
            i += 1
        return cells

    def clean(self, cell):
        contour = self.helpers.largestContour(cell.copy())
        x, y, w, h = cv2.boundingRect(contour)
        cell = self.helpers.make_it_square(cell[y:y + h, x:x + w], 28)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel)
        return 255 * (cell / 130)

    def centerDigit(self, digit):
        return self.centerY(self.centerX(digit))

    def centerX(self, digit):
        topLine = self.helpers.getTopLine(digit)
        bottomLine = self.helpers.getBottomLine(digit)
        if None in (topLine, bottomLine):
            return digit
        centerLine = (topLine + bottomLine) >> 1
        imageCenter = digit.shape[0] >> 1
        return self.helpers.rowShift(
            digit, start=topLine, end=bottomLine, length=imageCenter - centerLine)

    def centerY(self, digit):
        leftLine = self.helpers.getLeftLine(digit)
        rightLine = self.helpers.getRightLine(digit)
        if None in (leftLine, rightLine):
            return digit
        centerLine = (leftLine + rightLine) >> 1
        imageCenter = digit.shape[1] >> 1
        return self.helpers.colShift(
            digit, start=leftLine, end=rightLine, length=imageCenter - centerLine)
