import pickle
import xmlrpc.client

import matplotlib.pyplot
from PIL import Image
from pylab import *

server = xmlrpc.client.ServerProxy("http://localhost:8073")


def inv_color(image_array):
    pickle_image = pickle.dumps(image_array)
    binary_image = xmlrpc.client.Binary(pickle_image)
    response = server.send_back_inversion(binary_image)
    inverse_image_array = pickle.loads(response.data)
    return inverse_image_array


# Монохромное изображение
monochrome_image = Image.open('resources/11.bmp')
monochrome_image_array = array(monochrome_image)
matplotlib.pyplot.imshow(monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

inverse_monochrome_image_array = inv_color(monochrome_image_array)
matplotlib.pyplot.imshow(inverse_monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

# Цветное изображение
color_image = Image.open('resources/Jellyfish.jpg')
color_image_array = array(color_image)
matplotlib.pyplot.imshow(color_image, cmap="gray")
matplotlib.pyplot.show()

inverse_color_image_array = inv_color(color_image_array)
matplotlib.pyplot.imshow(inverse_color_image_array, cmap="gray")
matplotlib.pyplot.show()