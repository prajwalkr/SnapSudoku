import cv2
import numpy as np
import pickle

from helpers import Helpers
from grid import Grid
from cells import Cells


class Extractor(object):
    '''
        Stores and manipulates the input image to extract the Sudoku puzzle
    '''

    def __init__(self, path):
        '''
        1. Basic image manipulations - blur, thresholding.
        2. Crop out approx. sudoku puzzle (contour)
        3. Get the grid square vertices:
           3.1. Treat the image as a graph and find the largest
                                        connected component.
           3.2. This will be the gridlines image G, without the numbers.
           3.3. Compute the grid corners.
        5. Do a Warp perspective on both the gridlines image G,
           and the image with gridlines and numbers N.
        6. gridLess = (N - G); which is the image with only numbers
           and no grid lines. We will extract cells from this!
        '''
        self.helpers = Helpers()  # Image helpers
        self.image = self.loadImage(path)
        self.preprocess()
        sudoku = self.cropSudoku()
        grid = Grid(sudoku).grid 	# Grid of self.image
        sudoku, grid = self.straighten(sudoku, grid)
        gridLess = self.removeGridLines(sudoku, grid)
        self.cells = Cells(gridLess).cells

    def loadImage(self, path):
        color_img = cv2.imread(path)
        if color_img is None:
            raise IOError('Image not loaded')
        print 'Image loaded.'
        return color_img

    def preprocess(self):
    	print 'Preprocessing...',
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.medianBlur(self.image, 5)
        self.image = self.helpers.thresholdify(self.image)
        print 'done.'

    def cropSudoku(self):
    	print 'Cropping out Sudoku...',
        contour = self.helpers.largestContour(self.image.copy())
        sudoku = self.helpers.cut_out_sudoku_puzzle(self.image.copy(), contour)
        print 'done.'
        return sudoku

    def straighten(self, sudoku, grid):
    	print 'Straightening image...',
    	self.helpers.show(sudoku)
    	largest = self.helpers.largestContour(grid.copy())
        app = self.helpers.approx(largest)
        corners = self.helpers.get_rectangle_corners(app)
        sudoku = self.helpers.warp_perspective(corners, sudoku)
        grid = self.helpers.warp_perspective(corners, grid)
        print 'done.'
        return sudoku, grid

    def removeGridLines(self, sudoku, grid):
        H, W = grid.shape
        for i in xrange(W):
            for j in xrange(H):
                if grid[i][j] != 0:
                    sudoku[i][j] = 0
        return sudoku
