import cv2
import numpy as np

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

def make_it_square(image,side_length=300):
	return cv2.resize(image, (side_length,side_length))

def cut_out_sudoku_puzzle(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    return make_it_square(image[y:y + h, x:x + w])

def get_piece(image,side_length=28):
	return image[:side_length,:side_length]

def write_piece(image, row_beg,col_beg,row_end,col_end):
	cv2.imwrite('piece.jpg', image[row_beg:row_end,col_beg:col_end])

def get_largest_connected_component(image):
	res = None
	m = 0
	mpt = None
	visited = [[False for row in xrange(image.shape[0])] for col in xrange(image.shape[1])]
	for row in xrange(image.shape[0]):
		for col in xrange(image.shape[1]):
			if visited[row][col] == False:
				mask = np.zeros((image.shape[0] + 2,image.shape[1] + 2),np.uint8)
				cv2.floodFill(image.copy(), mask, (row,col), (255,255,255))
				if m < np.count_nonzero(mask):
					m = np.count_nonzero(mask)
					res = mask
					mpt = (row,col)
				visited |= mask[1:-1,1:-1]
	res *= 255
	return res[1:-1,1:-1]

def approx(cnt,grid):
	peri = cv2.arcLength(cnt, True)
	app = cv2.approxPolyDP(cnt, 0.02*peri, True)
	return app

def get_rectangle_corners(cnt):
	pts = cnt.reshape(4, 2)
	rect = np.zeros((4, 2), dtype = "float32")
	 
	# the top-left point has the smallest sum whereas the
	# bottom-right has the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	 
	# compute the difference between the points -- the top-right
	# will have the minumum difference and the bottom-left will
	# have the maximum difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

def warp_perspective(rect,grid):
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
		[0, maxHeight - 1]], dtype = "float32")
	 
	# calculate the perspective transform matrix and warp
	# the perspective to grab the screen
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(grid, M, (maxWidth, maxHeight))
	show(warp)
	return make_it_square(warp)

def get_sudoku_images(n=5):
    color_img = cv2.imread('sudoku1.jpg')					# read image
    gray_img = cv2.cvtColor(color_img,cv2.COLOR_BGR2GRAY)
    image = img = cv2.medianBlur(gray_img, 5)			# blur the image to reduce noise

    # adaptive-threshold the image `n` times
    image = thresholdify(image)

    # morphology the image to get accurate bounding rectangles
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    orig = image.copy()
    # crop out the sudoku puzzle from the image
    contour = get_largest_contour(image)
    sudoku = cut_out_sudoku_puzzle(orig, contour)

    orig = sudoku.copy()
    grid = get_largest_connected_component(sudoku.copy())
    app = approx(get_largest_contour(grid.copy()),grid.copy())
    corners = get_rectangle_corners(app)
    sudoku = warp_perspective(corners, sudoku)
    return orig, sudoku

orig, out = get_sudoku_images()
cv2.imwrite('orig.jpg', orig)
cv2.imwrite(str(101) + '.jpg', out)
