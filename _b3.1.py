from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

def adjust_color_balance(img, r_scale, g_scale, b_scale, gamma):
    """
    Adjusts the color balance of an image by multiplying each color value by a different
    user-specified constant, and applying a gamma transformation.
    
    Args:
    - img (PIL.Image.Image): The input image.
    - r_scale (float): The scaling factor for the red channel.
    - g_scale (float): The scaling factor for the green channel.
    - b_scale (float): The scaling factor for the blue channel.
    - gamma (float): The gamma correction factor.
    
    Returns:
    - The color-balanced image.
    """
    # Convert the input image to the RGB color space
    img = img.convert('RGB')
    
    # Create a lookup table for the gamma transformation
    lut = [int((i/255.0)**(1.0/gamma)*255) for i in range(256)]
    
    # Apply the color balance and gamma transformation
    r, g, b = img.split() # split img into tuple of 3 channel
    r = r.point(lambda x: lut[int(x*r_scale)]) # apply color intensity value for every point on image of that channel
    g = g.point(lambda x: lut[int(x*g_scale)])
    b = b.point(lambda x: lut[int(x*b_scale)])
    img = Image.merge('RGB', (r, g, b))
    
    return img

# Update the label with the color-balanced image whenever the sliders are moved
def update_image(*args):
    global img
    img_new = adjust_color_balance(img, r_scale.get(), g_scale.get(), b_scale.get(), gamma.get())
    photo = ImageTk.PhotoImage(img_new)
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.image = photo


# Create a Tkinter window with sliders for the color balance and gamma
def init():
    global root, r_scale, g_scale, b_scale, gamma, canvas, img
    root = tk.Tk()
    root.title('Color Balance')
    root.geometry('800x600')

    def get_fn_name():
        return filedialog.askopenfilename(title = 'Open')
    
    # Load an example image
    img = Image.open(get_fn_name())
    r_scale = tk.Scale(root, label='Red', from_=0.0, to=1.0, resolution=0.01, orient='horizontal')
    g_scale = tk.Scale(root, label='Green', from_=0.0, to=1.0, resolution=0.01, orient='horizontal')
    b_scale = tk.Scale(root, label='Blue', from_=0.0, to=1.0, resolution=0.01, orient='horizontal')
    gamma = tk.Scale(root, label='Gamma', from_=0.01, to=1.0, resolution=0.01, orient='horizontal')
    # if use pack instead of grid, the scale will be in a row
    r_scale.grid(column=0, row=0, rowspan=1)
    g_scale.grid(column=0, row=1, rowspan=1)
    b_scale.grid(column=0, row=2, rowspan=1)
    gamma.grid(column=0, row=3, rowspan=1)

    # Create a Tkinter label to display the color-balanced image
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.grid(column=1, row=0, rowspan=4)
    #must separate this two line    

    # Bind the sliders to the update_image function
    r_scale.config(command=update_image)
    g_scale.config(command=update_image)
    b_scale.config(command=update_image)
    gamma.config(command=update_image)



    

if __name__ == '__main__':
    init()
    # Run the Tkinter event loop
    root.mainloop()