
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale

    #flatten: 2d to 1d
    hist, bins = np.histogram(gray.flatten(),bins=256, range=[0, 256]) #calculate histogram
    #print(hist)
    for i in range(1, len(hist)):        
        hist[i] = hist[i] + hist[i-1] #h(i) = h(i) + h(i-1) theo formula 3.9 sach 
        # hist[i] tai sao ko lon hon tong hist duoc hay vi no la histogram

    #compute transfer function or normalize value        
    cdf = hist / sum(hist) #h(i) / total pixels
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min()) #normalize value or transfer function
    #print(cdf_normalized)


    #apply transfer function to image
    print(gray.shape)
    result = cdf_normalized[gray] 
    #tuong ung result = cdf_normalized[gray[i,j]] value la index cua cdf_normalized
    #cdf_normalize tu 0 den 255
    re_hist, re_bins = np.histogram(result.flatten(), 256, [0, 256])

    plt.subplot(2,2,1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original")

    plt.subplot(2,2,3)
    plt.hist(gray.flatten(),bins=range(0, 256), color='r')
    plt.title("Histogram of original")

    plt.subplot(2,2,2)
    plt.imshow(result, cmap='gray')
    plt.title('Equalized')

    plt.subplot(2,2,4)
    plt.plot(hist,color='b')
    plt.title("Histogram of equalized")
    plt.tight_layout()
    plt.show()

    return result


img = cv2.imread("./Bear.jpg")
histogram_equalization(img)



