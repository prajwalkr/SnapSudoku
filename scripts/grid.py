import cv2
import numpy as np
import Queue

class Grid(object):
    '''
            Extracts out the gridlines from a sudoku image and returns Grid obj.
            Implements the classic `Largest connected component` algorithm.
    '''

    def __init__(self, image):
        self.graph = image.copy()
        self.W, self.H = self.graph.shape
        self.visited = [[False for _ in xrange(
            self.H)] for _ in xrange(self.W)]
        self.grid = [[None for _ in xrange(self.H)] for _ in xrange(self.W)]
        self.buildGrid()

    def buildGrid(self):
        componentId = 0
        for i in xrange(self.H):
            for j in xrange(self.W):
                if not self.visited[i][j]:
                    self.bfs(i, j, componentId)
                    componentId += 1
        componentSizes = [0 for _ in xrange(componentId)]
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    componentSizes[cell] += 1
        largest = componentSizes.index(max(componentSizes))
        for i in xrange(self.H):
            for j in xrange(self.W):
                self.grid[i][j] = 255 if self.grid[i][j] == largest else 0
        self.grid = np.asarray(self.grid, dtype=np.uint8)

    def bfs(self, i, j, num):
        q = Queue.Queue()
        q.put((i, j))
        while not q.empty():
            i, j = q.get()
            inValidRow = i not in xrange(0, self.H)
            inValidCol = j not in xrange(0, self.W)
            invalidCell = inValidRow or inValidCol
            invalidPixel = invalidCell or self.graph[i][j] != 255
            if invalidPixel or self.visited[i][j]:
                continue
            self.grid[i][j] = num
            self.visited[i][j] = True
            q.put((i, j + 1))
            for dj in [-1, 0, 1]:
                q.put((i + 1, j + dj))
