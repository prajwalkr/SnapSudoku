import cv2
import numpy as np
import train as t
import pickle
from os import path


def show(img):
    screen_res = 1280, 720
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)

    cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('dst_rt', window_width, window_height)

    cv2.imshow('dst_rt', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def thresholdify(img):
    img = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 41, 3)
    return 255 - img


def dilate(image, kernel):
    cv2.dilate(image, kernel)
    return image


def get_largest_contour(image):
    contours, h = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea)


def make_it_square(image, side_length=306):
    return cv2.resize(image, (side_length, side_length))

def area(image):
	return float(image.shape[0]*image.shape[1])

def cut_out_sudoku_puzzle(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    return make_it_square(image[y:y + h, x:x + w])


def binarized(image):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i][j] = 255 * int(image[i][j] != 255)
    # show(image)
    return image


def is_greater_connected_component(mask, m, half_image_area):
    pixel_count = np.count_nonzero(mask)
    component_area = cv2.contourArea(get_largest_contour(mask))
    return (m < pixel_count and component_area > half_image_area)


def get_largest_connected_component(image):
    image = binarized(image)
    res = None
    m = 0
    W,H = image.shape
    half_image_area = area(image) / 2.00
    for row in xrange(H):
        for col in xrange(W):
            if image[row][col] == 255:
                mask = np.zeros(
                    (W + 2, H + 2), np.uint8)
                flags = cv2.FLOODFILL_FIXED_RANGE
                cv2.floodFill(image.copy(), mask, (row, col),
                              (255, 255, 255), flags=flags)
                if is_greater_connected_component(mask, m, half_image_area):
                    m = np.count_nonzero(mask)
                    res = mask
    res *= 255
    return res[1:-1, 1:-1]


def extract_digit(cell):
    orig = cell.copy()
    contours, h = cv2.findContours(
        cell, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        cv2.drawContours(cell, [cnt], 0, (255, 0, 0), 1)
        cell = orig


def clean(cell, n=5):
    for _ in range(n):
        kernel = np.ones((3, 3), np.uint8)
        cv2.erode(cell, kernel)
    return 255 - cell


def approx(cnt, grid):
    peri = cv2.arcLength(cnt, True)
    app = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    return app

def is_warp_needed(image):
	return (cv2.contourArea(get_largest_contour(image)) < 0.90 * (area(image)))

def get_rectangle_corners(cnt):
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


def warp_perspective(rect, grid):
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
    return make_it_square(warp)


def get_cells(sudoku):
    cells = []
    W,H = sudoku.shape
    cell_size = W / 9
    for r in range(0, W, cell_size):
        row = []
        for c in range(0, W, cell_size):
            cell = make_it_square(sudoku[r:r + cell_size, c:c + cell_size], 28)
            cell = clean(cell)
            row.append(cell)
            show(cell)
        cells.append(row)
    return cells


def evaluate(cells):
    net = None
    with open('test', 'rb') as f:
        net = pickle.load(f)

    res = []
    for i, r in enumerate(cells):
        row = []
        for j, image in enumerate(r):
            im = image.ravel().astype(np.float64)
            im = 1 - im * (1.0 / 255.0)
            im = np.reshape(im, (784, 1))
            with open('mat.txt', 'w') as f:
                f.write('\n'.join(str(i) for i in im))
            outputs = net.feedforward(im)
            print(i, j), max(outputs), np.argmax(outputs)
            x = raw_input()


def update_dataset(cells):
    data = None
    if path.exists('/train/dataset'):
        with open('test', 'rb') as f:
            data = pickle.load(f)
    data = [] if data is None else data
    for r in cells:
        for image in r:
            show(image)
            im = image.ravel().astype(np.float64)
            im = 1 - im * (1.0 / 255.0)
            im = np.reshape(im, (784, 1))
            res = None
            while res not in xrange(-1, 10):
                try:
                    res = int(raw_input())
                except:
                    pass
            data.append(im)
    with open('/train/dataset') as f:
        pickle.dump(data, f)


def remove_lines(sudoku, grid):
    H = grid.shape[0]
    W = grid.shape[1]
    for i in xrange(W):
        for j in xrange(H):
            if grid[i][j] != 0:
                sudoku[i][j] = 0
    return sudoku


def main():
    IMAGE_DIR = path.join(path.dirname(__file__), 'train/')
    done = None
    if path.exists('/train/done'):
        with open('/train/done', 'rb') as f:
            done = pickle.load(f)
    else:
        done = []

    for i in range(22):
        if i in done:
            continue
        #color_img = cv2.imread(
        #    path.join(IMAGE_DIR, '{}.jpg'.format(str(i))))		# read image
        color_img = cv2.imread('image1.jpg')
        if color_img is None:
            raise Exception('Image not loaded')
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        # blur the image to reduce noise
        image = img = cv2.medianBlur(gray_img, 5)

        # adaptive-threshold the image `n` times
        image = thresholdify(image)

        # morphology the image to get accurate bounding rectangles
        kernel = np.ones((3, 3), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        orig = image.copy()
        # crop out the sudoku puzzle from the image
        contour = get_largest_contour(image)
        sudoku = cut_out_sudoku_puzzle(orig, contour)
        print area(sudoku)
        show(sudoku)
        orig = sudoku.copy()
        grid = get_largest_connected_component(sudoku.copy())
        print cv2.contourArea(get_largest_contour(grid.copy()))
        show(grid)
        app = approx(get_largest_contour(grid.copy()), grid.copy())
        corners = get_rectangle_corners(app)
        sudoku = warp_perspective(corners, sudoku)
        grid = warp_perspective(corners, grid)
        show(grid)
        show(sudoku)
        sudoku = remove_lines(sudoku, grid)
        show(sudoku)
        cells = get_cells(sudoku)
        update_dataset(cells)
        done.append(i)
        with open('/train/done', 'wb') as f:
            pickle.dump(done, f)
        # evaluate(cells)

main()
