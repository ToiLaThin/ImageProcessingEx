import cv2
import numpy as np
from matplotlib import pyplot as plt

# read image
img = cv2.imread('./Lenna.png')

# apply Gaussian blur
blur = cv2.GaussianBlur(img, (5,5), 0)

# apply median filter
median = cv2.medianBlur(img, 5)

# apply Laplacian filter for sharpening
laplacian = cv2.Laplacian(img, cv2.CV_64F)

# plot images
plt.subplot(2,2,1),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(blur),plt.title('Gaussian Blur')
plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(median),plt.title('Median Filter')
plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(laplacian),plt.title('Laplacian Filter')
plt.xticks([]), plt.yticks([])

plt.show()