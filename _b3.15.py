
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

#only for binary image
def city_block_distance_transform(image):
    rows, cols = image.shape
    result = np.zeros((rows, cols), dtype=np.float32)

    # Forward pass
    for i in range(rows):
        for j in range(cols):
            if image[i, j] != 0:
                result[i, j] = np.min([result[i-1, j], result[i, j-1]]) + 1

    # Backward pass
    for i in range(rows-1, -1, -1):
        for j in range(cols-1, -1, -1):
            if image[i, j] != 0:
                result[i, j] = np.min([result[i, j], result[i+1, j]+1, result[i, j+1]+1])

    temp_img = np.hstack((image, result))
    return temp_img

def euclidean_distance_transform(image):
    rows, cols = image.shape
    result = np.zeros((rows, cols), dtype=np.float32)

    # Forward pass
    for i in range(rows):
        for j in range(cols):
            if image[i, j] != 0:
                # if i == 0 and j == 0:
                #     result[i, j] = 0
                # elif i == 0:
                #     result[i, j] = result[i, j-1] + 1
                # elif j == 0:
                #     result[i, j] = result[i-1, j] + 1
                # else:
                result[i, j] = np.sqrt(2) + np.min([result[i-1, j-1], result[i-1, j], result[i, j-1]])

    # Backward pass
    for i in range(rows-1, -1, -1):
        for j in range(cols-1, -1, -1):
            if image[i, j] != 0:
                # if i == rows-1 and j == cols-1:
                #     pass
                # elif i == rows-1:
                #     result[i, j] = np.min([result[i, j], result[i, j+1] + 1])
                # elif j == cols-1:
                #     result[i, j] = np.min([result[i, j], result[i+1, j] + 1])
                # else:
                result[i, j] = np.min([result[i, j], np.sqrt(2) + result[i+1, j+1], result[i+1, j] + 1, result[i, j+1] + 1])

    #print("Original",img)
    #print("Transformed",result)
    # for intensity_pix in result.flatten():
    #     print(intensity_pix)
    temp_img = np.hstack((image, result))
    return temp_img

img = cv2.imread("./Bear.jpg", cv2.IMREAD_GRAYSCALE)
ret, thresh_binary_img = cv2.threshold(img, 40,555, type=cv2.THRESH_BINARY)
res = euclidean_distance_transform(thresh_binary_img)
cv2.imshow("Result", res)
cv2.waitKey(0)
cv2.destroyAllWindows()



