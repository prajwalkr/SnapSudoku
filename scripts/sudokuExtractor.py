import cv2
import numpy as np
import pickle

from helpers import Helpers
from cells import Cells
    

class Extractor(object):
    '''
        Stores and manipulates the input image to extract the Sudoku puzzle
        all the way to the cells
    '''

    def __init__(self, path):
        self.helpers = Helpers()  # Image helpers
        self.image = self.loadImage(path)
        self.preprocess()
        #self.helpers.show(self.image, 'After Preprocessing')
        sudoku = self.cropSudoku()
        #self.helpers.show(sudoku, 'After Cropping out grid')
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
