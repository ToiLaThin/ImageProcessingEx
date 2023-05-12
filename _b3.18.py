import numpy as np
import cv2

#upsample using nearest neighbor interpolation(insert-like)
def nearest_neighbor_interpolation(path:str, scale):
    input_img = cv2.imread(path)
    img = input_img.copy()
    height, width = img.shape[:2]
    new_height, new_width = int(height*scale), int(width*scale)
    new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for i in range(new_height):
        for j in range(new_width):
            #x, y coords in old img or neighbors
            x, y = int(round(i/scale)), int(round(j/scale))
            new_img[i, j] = img[x, y]
    return new_img

#upsample using linear interpolation
def linear_interpolation(path:str, scale):
    input_img = cv2.imread(path)
    img = input_img.copy()
    height, width = img.shape[:2]
    new_height, new_width = int(height*scale), int(width*scale)
    new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for i in range(new_height):
        for j in range(new_width):
            x, y = i/scale, j/scale
            x1, y1 = int(np.floor(x)), int(np.floor(y))
            x2, y2 = int(np.ceil(x)), int(np.ceil(y))
            if x2 >= height:
                x2 = height - 1
            if y2 >= width:
                y2 = width - 1
            alpha = x - x1
            beta = y - y1

            #\ for mulitline output
            new_img[i, j] = (1-alpha)*(1-beta)*img[x1, y1] + \
                            alpha*(1-beta)*img[x2, y1] + \
                            (1-alpha)*beta*img[x1, y2] + \
                            alpha*beta*img[x2, y2]
    return new_img

#downsample using decimation
def decimation(path:str, scale:int):
    input_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = input_img.copy()
    height, width = img.shape[:2]

    #define kernal size 2x2x3 (or 2x2 if gray scale) of 1/4
    kernel = np.ones((2,2), dtype=np.float32) / 4
    print("kernel: ", kernel)
    print("kernel shape: ", kernel.shape)
    #init empty array with new size
    downsampled_img = np.zeros((int(height//scale), int(width//scale)), dtype=np.uint8)
    for i in range(0, height, scale):
        for j in range(0, width, scale):
            block = img[i:i+2,j:j+2]
            if i == 2  and j == 2:
                print("block: ", block)
                print('block shape:', block.shape)
            downsampled_img[i//scale, j//scale] = np.sum(kernel * block) // np.sum(kernel)#convolution 2 matrix

    return downsampled_img


input_img = cv2.imread("./Lenna.png")
output_img_linear = linear_interpolation("./Lenna.png", 1.5)
output_img_neighbor = nearest_neighbor_interpolation("./Lenna.png", 1.5)
output_img_decimation = decimation("./Lenna.png", 2)
cv2.imshow("Input", input_img)
#cv2.imshow("Result Linear", output_img_linear)
cv2.imshow("Result Nearest Neighbor", output_img_neighbor)
#cv2.imshow("Result Decimation", output_img_decimation)
cv2.waitKey(0)
cv2.destroyAllWindows()