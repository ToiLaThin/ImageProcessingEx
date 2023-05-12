from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

def contrast(image, level):
    """
    Adjusts the contrast of an image.

    Parameters:
        - image: input image as a NumPy array
        - level: contrast level (range: -100 to 100)

    Returns:
        - output image as a NumPy array
    """
    #linear contrast scaler
    #f = 255 * level / 200 

    #contrast stretching scaler
    #new_pixel_value = (pixel_value - min_pixel_value) * (new_max - new_min) / (max_pixel_value - min_pixel_value) + new_min
    #max: 127 + 131 = 258 min: 127
    
    #non-linear contrast scaler f is actually alpha
    f = (131 * (level + 127)) / (127 * (131 - level))
    alpha_c = f + 1
    gamma_c = 127 * (1 - f) # the more contrast, the more dark when f > 1 -> darker 
    np_img = np.array(image)
    print("F", f, sep=": ")
    print("Level:", level, sep=": ")
    print("Alpha each pixels", alpha_c, sep=": ")
    print("Gamma each pixels", gamma_c, sep=": ")
    #https://docs.opencv.org/3.4/d5/dc4/tutorial_adding_images.html
    output = cv2.addWeighted(np_img, alpha_c, np_img, 0, gamma_c)
    #ouput = alpha_c * np_img + gamma_c # second src is mulitplied by 0
    return output

def contrast_alt(image, level):
    
    factor = (259 * (level + 255)) / (255 * (259 - level))
    alpha_c = factor

    #gamma_c = 0  no change is not contrast because light -> lighter dark -> darker is called contrast
    #so the dark will be darker and the light will be lighter
    gamma_c = 69 * (1 - factor)

    np_img = np.array(image)
    output = cv2.addWeighted(np_img, alpha_c, np_img, 0, gamma_c)
    return output

def solarize(image, threshold):
    """
    Applies solarization effect to an image.

    Parameters:
        - image: input image as a NumPy array
        - threshold: threshold value (range: 0 to 255)

    Returns:
        - output image as a NumPy array
    """
    temp_img = np.array(image)
    output = np.zeros(temp_img.shape, np.uint8)
    output[temp_img < threshold] = temp_img[temp_img < threshold]
    output[temp_img >= threshold] = threshold#255 - temp_img[temp_img >= threshold]

    # dam bao toan bo pixel cua image < threshhold
    return output
    #return cv2.bitwise_not(temp_img)

# Update the label with the color-balanced image whenever the sliders are moved
def update_image_contrast(*args):
    global img
    img_new = Image.fromarray(contrast_alt(img, contrast_level.get()))
    photo = ImageTk.PhotoImage(img_new)
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.image = photo

def update_image_solarize(*args):
    global img
    img_new = Image.fromarray(solarize(img, solarize_threshhold_pixel_value.get()))
    photo = ImageTk.PhotoImage(img_new)
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.image = photo


# Create a Tkinter window with sliders for the color balance and gamma
def init():
    global root, contrast_level, solarize_threshhold_pixel_value, canvas, img
    root = tk.Tk()
    root.title('Adjust Contrast and Solarizatoin')
    root.geometry('800x600')

    def get_fn_name():
        return filedialog.askopenfilename(title = 'Open')
    
    # Load an example image
    img = Image.open(get_fn_name())
    contrast_level = tk.Scale(root, label='Contrast level', from_=-100, to=200, resolution=1, orient='horizontal')
    solarize_threshhold_pixel_value = tk.Scale(root, label='Threshold pixel value', from_=100, to=200, resolution=1, orient='horizontal')
    # if use pack instead of grid, the scale will be in a row
    contrast_level.grid(column=0, row=0, rowspan=1)
    solarize_threshhold_pixel_value.grid(column=0, row=1, rowspan=1)

    # Create a Tkinter label to display the color-balanced image
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.grid(column=1, row=0, rowspan=4)
    #must separate this two line    

    # Bind the sliders to the update_image function
    contrast_level.config(command=update_image_contrast)
    solarize_threshhold_pixel_value.config(command=update_image_solarize)


    

if __name__ == '__main__':
    init()
    # Run the Tkinter event loop
    root.mainloop()