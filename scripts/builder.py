import pickle
import os
import numpy as np

from sudokuExtractor import Extractor


class Builder(object):
    '''
    Builds dataset from images in a folder.
    '''

    def __init__(self, imgDir=None, rebuild=False):
        if imgDir is None:
            ROOT = os.path.dirname(os.getcwd())
            self.imgDir = os.path.join(ROOT, 'train/')
        else:
            self.imgDir = os.path.abspath(imgDir)

        self.usedSet = dict()
        if rebuild == False:
            usedSetPath = os.path.join(os.getcwd(), 'usedSet')
            if os.path.exists(usedSetPath):
                self.usedSet = pickle.load(open(usedSetPath, 'r'))

        if len(self.usedSet) == 0:
            self.trainingData = []
            self.testingData = []
        else:
            self.trainingData = pickle.load(open('train', 'r'))
            self.testingData = pickle.load(open('test', 'r'))

        try:
            for imagePath, results, file in self.getUnusedImages():
                cells = Extractor(imagePath).cells
                trainingInputs = [
                    [np.reshape(cell, (784, 1)) for cell in row] for row in cells]
                trainingResults = [[self.vectorizedResult(
                    int(digit)) for digit in row] for row in results]
                for i in xrange(9):
                    for j in xrange(9):
                        if trainingResults[i][j] == None:
                            continue
                        self.trainingData.append(
                            (trainingInputs[i][j], trainingResults[i][j]))
                        self.testingData.append(
                            (trainingInputs[i][j], int(results[i][j])))
                self.usedSet[file] = True

        except:
            self.saveData()
            raise
        self.saveData()

    def getUnusedImages(self):
        for file in os.listdir(self.imgDir):
            if file.endswith('.jpg') and file not in self.usedSet:
                imagePath = os.path.join(self.imgDir, file)
                resultPath = os.path.join(self.imgDir, file[:-3] + 'dat')
                results = None
                try:
                    with open(resultPath, 'r') as resFile:
                        results = [list(row)
                                   for row in resFile.read().splitlines()]
                except IOError:
                    continue
                yield (imagePath, results, file)

    def vectorizedResult(self, j):
        if j == 0:
            return None
        e = np.zeros((10, 1))
        e[j] = 1.0
        return e

    def saveData(self):
        pickle.dump(self.usedSet, open('usedSet', 'w'))
        pickle.dump(self.trainingData, open('train', 'w'))
        pickle.dump(self.testingData, open('test', 'w'))

Builder()