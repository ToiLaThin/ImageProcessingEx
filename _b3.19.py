import numpy as np
import cv2

def decimation(input_img, scale:int ,kernel):
    img = input_img.copy()
    height, width = img.shape[:2]

    #init empty array with new size
    downsampled_img = np.zeros((int(height//scale), int(width//scale)), dtype=np.uint8)
    #1d array -> 2d array
    if len(kernel.shape) == 1: 
        kernel = np.reshape(kernel,(1, kernel.shape[0]))
    #valid because prev line    
    k_h, k_w = kernel.shape[:2] #print(kernel.shape)
    for i in range(0, height, scale):
        for j in range(0, width, scale):
            block = img[i:i+k_h,j:j+k_w]
            if block.shape == kernel.shape:
                downsampled_img[i//scale, j//scale] = np.sum(kernel * block) // np.sum(kernel)
            else: downsampled_img[i//scale, j//scale] = img[i,j]

    return downsampled_img

def pyramid(path, levels, kernel):
    input_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = input_img.copy()

    # create an array to hold the pyramid levels
    pyramid = [img]
    scale = 2
    # generate the pyramid levels by downsampling the image
    for i in range(levels - 1):
        level_img = decimation(pyramid[i], scale, kernel)
        pyramid.append(level_img)
    return pyramid


bionominal_kernel = np.array([1, 4, 6 ,4 ,1])
bionominal_kernel = bionominal_kernel * 1/16

x2kernel = np.ones((2,2), dtype=np.float32) / 4

pyramid_img_lst = pyramid("./Lenna.png", 4, kernel=bionominal_kernel)
for idx, p_img in enumerate(pyramid_img_lst, 1):
    cv2.imshow(f"Pyramid layer {idx}",p_img)
    cv2.waitKey(0)
cv2.destroyAllWindows()