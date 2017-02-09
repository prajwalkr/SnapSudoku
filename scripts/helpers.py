import cv2
import numpy as np

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3


class Helpers(object):
    '''
    Image manipulation helper functions
    '''

    def show(self, img, windowName='Image'):
        screen_res = 1280.0, 720.0
        scale_width = screen_res[0] / img.shape[1]
        scale_height = screen_res[1] / img.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(img.shape[1] * scale)
        window_height = int(img.shape[0] * scale)

        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, window_width, window_height)

        cv2.imshow(windowName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def isCv2(self):
        print(cv2.__version__)
        return cv2.__version__.startswith('2.')

    def thresholdify(self, img):
        img = cv2.adaptiveThreshold(img.astype(np.uint8), 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 11, 3)
        return 255 - img

    def Canny(self, image):
        edges = cv2.Canny(image, 100, 200)
        self.show(edges)
        return edges

    def dilate(self, image, kernel):
        cv2.dilate(image, kernel)
        return image

    def getContours(self, image):
        """In OpenCV v2.x cv2.findContours returns contours, hierarchy.
           In OpenCV v3.x cv2.findContours returns image, contours, hierarchy.
           In both v2.x & v3.x contours is in postion [-2] of return values."""
        return cv2.findContours(image, cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]  # second last

    def largestContour(self, image):
        contours = self.getContours(image)
        return max(contours, key=cv2.contourArea)

    def largest4SideContour(self, image):
        contours = self.getContours(image)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for cnt in contours[:min(5, len(contours))]:
            # im = image.copy()
            # cv2.drawContours(im, cnt, -1, (255,255,255), 5)
            # self.show(im,'contour')
            if len(self.approx(cnt)) == 4:
                return cnt
        return None

    def make_it_square(self, image, side_length=306):
        return cv2.resize(image, (side_length, side_length))

    def area(self, image):
        return float(image.shape[0] * image.shape[1])

    def cut_out_sudoku_puzzle(self, image, contour):
        x, y, w, h = cv2.boundingRect(contour)
        image = image[y:y + h, x:x + w]
        return self.make_it_square(image, min(image.shape))

    def binarized(self, image):
        for i in xrange(image.shape[0]):
            for j in xrange(image.shape[1]):
                image[i][j] = 255 * int(image[i][j] != 255)
        return image

    def approx(self, cnt):
        peri = cv2.arcLength(cnt, True)
        app = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        return app

    def get_rectangle_corners(self, cnt):
        pts = cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point has the smallest sum whereas the
        # bottom-right has the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # compute the difference between the points -- the top-right
        # will have the minumum difference and the bottom-left will
        # have the maximum difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def warp_perspective(self, rect, grid):
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        # ...and now for the height of our new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

        # take the maximum of the width and height values to reach
        # our final dimensions
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        M = cv2.getPerspectiveTransform(rect, dst)
        warp = cv2.warpPerspective(grid, M, (maxWidth, maxHeight))
        return self.make_it_square(warp)

    def getTopLine(self, image):
        for i, row in enumerate(image):
            if np.any(row):
                return i
        return None

    def getBottomLine(self, image):
        for i in xrange(image.shape[0] - 1, -1, -1):
            if np.any(image[i]):
                return i
        return None

    def getLeftLine(self, image):
        for i in xrange(image.shape[1]):
            if np.any(image[:, i]):
                return i
        return None

    def getRightLine(self, image):
        for i in xrange(image.shape[1] - 1, -1, -1):
            if np.any(image[:, i]):
                return i
        return None

    def rowShift(self, image, start, end, length):
        shifted = np.zeros(image.shape)
        if start + length < 0:
            length = -start
        elif end + length >= image.shape[0]:
            length = image.shape[0] - 1 - end

        for row in xrange(start, end + 1):
            shifted[row + length] = image[row]
        return shifted

    def colShift(self, image, start, end, length):
        shifted = np.zeros(image.shape)
        if start + length < 0:
            length = -start
        elif end + length >= image.shape[1]:
            length = image.shape[1] - 1 - end

        for col in xrange(start, end + 1):
            shifted[:, col + length] = image[:, col]
        return shifted
