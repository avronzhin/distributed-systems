import pickle
import xmlrpc.client

import matplotlib.pyplot
from PIL import Image
from pylab import *

server = xmlrpc.client.ServerProxy("http://localhost:8071")


def rotate_image(image_array):
    pickle_image = pickle.dumps(image_array)
    binary_image = xmlrpc.client.Binary(pickle_image)
    response = server.rotate(binary_image)
    rotated_image_array = pickle.loads(response.data)
    return rotated_image_array


# Монохромное изображение
monochrome_image = Image.open('resources/11.bmp')
monochrome_image_array = array(monochrome_image)
matplotlib.pyplot.imshow(monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

rotated_monochrome_image_array = rotate_image(monochrome_image_array)
matplotlib.pyplot.imshow(rotated_monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

# Цветное изображение
color_image = Image.open('resources/Jellyfish.jpg')
color_image_array = array(color_image)
matplotlib.pyplot.imshow(color_image, cmap="gray")
matplotlib.pyplot.show()

rotated_color_image_array = rotate_image(color_image_array)
matplotlib.pyplot.imshow(rotated_color_image_array, cmap="gray")
matplotlib.pyplot.show()