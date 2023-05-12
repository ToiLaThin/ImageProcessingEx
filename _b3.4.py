import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the background and foreground images
foreground = cv2.imread('.\\pizza_bluescreen.jpg')
foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB)
lower_blue_threshold = np.array([0,0,230])
upper_blue_threshold = np.array([255,255,255])
mask = cv2.inRange(foreground, lower_blue_threshold, upper_blue_threshold)
print((mask[0][1]).shape)
masked_foreground = np.copy(foreground)
masked_foreground[mask != 0] = [0, 0, 0] # vi rgb nen tai (x,y) ma tai do mask cung = 0
#plt.imshow(masked_foreground)


#compositing new background
new_background = cv2.imread("dongtien.png")
print("Background shape:", new_background.shape)
print("Foreground shape:", masked_foreground.shape)
masked_foreground = cv2.resize(masked_foreground, (new_background.shape[0], new_background.shape[1]))
new_background = cv2.cvtColor(new_background, cv2.COLOR_BGR2RGB)
new_background[masked_foreground != 0] = 0
# plt.imshow(new_background)

# new_composited_img = cv2.addWeighted(masked_foreground, 1, new_background, 1, 0)
new_composited_img = 1 * new_background + masked_foreground 
plt.imshow(new_composited_img)
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()
