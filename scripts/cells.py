import numpy as np
import cv2

from helpers import Helpers
from digit import Digit


class Cells(object):
    '''
    Extracts each cell from the sudoku grid obtained
    from the Extractor
    '''

    def __init__(self, gridLess):
        print 'Extracting cells...',
        self.helpers = Helpers()
        self.cells = self.extractCells(gridLess)
        print 'done.'

    def extractCells(self, sudoku):
        cells = []
        W, H = sudoku.shape
        cell_size = W / 9
        for r in range(0, W, cell_size):
            row = []
            for c in range(0, W, cell_size):
                cell = self.helpers.make_it_square(
                    sudoku[r:r + cell_size, c:c + cell_size], 28)
                cell = self.clean(cell)
                digit = Digit(cell).digit
                row.append(digit)
                self.helpers.show(digit,'Digit')
            cells.append(row)
        return cells

    def clean(self, cell):
        contour = self.helpers.largestContour(cell.copy())
        x, y, w, h = cv2.boundingRect(contour)
        cell = self.helpers.make_it_square(cell[y:y + h, x:x + w], 28)
        cell = 255 * (cell / 150)
        return cell
