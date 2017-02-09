### Algorithm

 - Basic image preprocessing - **Thresholding**
 - Crop out approx. Sudoku puzzle (largest contour)
 - Get the grid square verticles (*need for improvement*)
    - Get the largest contour of the image
    - Get the largest bounding rectangle within the contour
    - Compute the grid corners
 - Do a **warp perspective** on the Sudoku
 - Extract cells by slicing the grid evenly
 - Isolate cells as follows
    - Extract the largest connected component, giving more priority to the center pixels
    - Remove all major noise in a cell
 - Predict digits using a Neural Network
