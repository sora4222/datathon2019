I want to brighten all the masks but such that they are still relative to
each other.
Goal 1: Find the brightest pixel in one band. ----- Done
convert image into greys
convert the images into a stream of np.ndarrays
reduce them to the brightest pixel

Goal 2:
The brightest pixel needs to come up to 255 the brightest value unless 0


https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html