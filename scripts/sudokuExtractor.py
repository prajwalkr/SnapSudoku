import cv2
import numpy as np
import pickle

from helpers import Helpers
from cells import Cells


class Extractor(object):
    '''
        Stores and manipulates the input image to extract the Sudoku puzzle
    '''

    def __init__(self, path):
        '''
        1. Basic image manipulations - Thresholding.
        2. Crop out approx. sudoku puzzle (contour)
        3. Get the grid square vertices:
           3.1. Get the largest contour of the image.
           3.2. Get the largest bounding rectangle within the contour.
           3.3. Compute the grid corners.
        5. Do a Warp perspective on the sudoku image. 
        6. We will extract cells from this, by slicing the sudoku grid evenly.
        7. Digit isolation in cell is done through a series of steps:
            7.1. Extracting the largest connected component in the image,
                 giving more priority to the center pixels.
            7.2. Removing all major noise in the cell. 
            7.3. Centering of digits after extraction. 
        '''
        self.helpers = Helpers()  # Image helpers
        self.image = self.loadImage(path)
        self.preprocess()
        #self.helpers.show(self.image, 'After Preprocessing')
        sudoku = self.cropSudoku()
        sudoku = self.straighten(sudoku)
        #self.helpers.show(sudoku, 'Final Sudoku grid')
        self.cells = Cells(sudoku).cells

    def loadImage(self, path):
        color_img = cv2.imread(path)
        if color_img is None:
            raise IOError('Image not loaded')
        print 'Image loaded.'
        return color_img

    def preprocess(self):
        print 'Preprocessing...',
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = self.helpers.thresholdify(self.image)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
        print 'done.'

    def cropSudoku(self):
        print 'Cropping out Sudoku...',
        contour = self.helpers.largestContour(self.image.copy())
        sudoku = self.helpers.cut_out_sudoku_puzzle(self.image.copy(), contour)
        print 'done.'
        return sudoku

    def straighten(self, sudoku):
        print 'Straightening image...',
        largest = self.helpers.largest4SideContour(sudoku.copy())
        app = self.helpers.approx(largest)
        corners = self.helpers.get_rectangle_corners(app)
        sudoku = self.helpers.warp_perspective(corners, sudoku)
        print 'done.'
        return sudoku
