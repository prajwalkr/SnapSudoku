import os
import pickle
import numpy as np

from sudokuExtractor import Extractor

def load(filename):
    with open(filename) as in_file:
        return pickle.load(in_file)

def dump(data, filename):
    with open(filename, 'w') as out_file:
        pickle.dump(data, out_file)


class Builder(object):
    '''
    Builds dataset from images in a folder.
    '''

    def __init__(self, imgDir=None, rebuild=False):
        self.imgDir = (os.path.abspath(imgDir) if imgDir else
            os.path.join(os.path.dirname(os.getcwd()), 'train/'))
        self.usedSet = {}
        if rebuild == False:
            usedSetPath = os.path.join(os.getcwd(), 'usedSet')
            if os.path.exists(usedSetPath):
                self.usedSet = load(usedSetPath)
        self.trainingData = load('train') if self.usedSet else []
        self.testingData = load('test') if self.usedSet else []

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
        dump(self.usedSet, 'usedSet')
        dump(self.trainingData, 'train')
        dump(self.testingData, 'test')

Builder()
