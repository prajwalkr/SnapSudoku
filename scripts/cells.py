import numpy as np

from helpers import Helpers


class Cells(object):
    '''
            Extracts each cell from the gridLess image obtained
            from the Extractor
    '''

    def __init__(self, gridLess):
        print 'Extracting cells...',
        self.helpers = Helpers()
        self.cells = self.extractCells(gridLess)
        print 'done.'

    def extractCells(self,sudoku):
        cells = []
        W, H = sudoku.shape
        cell_size = W / 9
        for r in range(0, W, cell_size):
            row = []
            for c in range(0, W, cell_size):
                cell = self.helpers.make_it_square(
                    sudoku[r:r + cell_size, c:c + cell_size], 28)
                cell = self.helpers.clean(cell)
                row.append(cell)
            cells.append(row)
        return cells
