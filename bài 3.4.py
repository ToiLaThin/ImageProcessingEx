import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
# matplotlib inline

def change_background(image):
      
      
      #print('This image is:', type(image), 
       #     ' with dimensions:', image.shape)

      image_copy = np.copy(image)
      

      image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
      

      lower_blue = np.array([0,0,230])  
      upper_blue = np.array([250,250,255])

      mask = cv2.inRange(image_copy, lower_blue, upper_blue)
      plt.imshow(mask, cmap='gray')

      masked_image = np.copy(image_copy)
      masked_image[mask != 0] = [0, 0, 0]
      plt.imshow(masked_image)

      background_image = np.zeros(image.shape, np.uint8)
      background_image[:] = (0, 0, 0)

      background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
      crop_background = background_image[0:image.shape[0], 0:image.shape[1]]


      crop_background[mask == 0] = [0,0,0]
      #plt.imshow(crop_background)

      complete_image = masked_image + crop_background
      #plt.imshow(complete_image)
      #plt.show()
      return complete_image


file_image='pizza_bluescreen.jpg'


img=cv2.imread(file_image)
titles = ["Origin",'Removebackground']
images = [img,change_background(img)]
plt.figure(figsize=(13,5))
for i in range(2):
    plt.subplot(2,2,i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])


plt.tight_layout()
plt.show()







