import pickle
import xmlrpc.client

import matplotlib.pyplot
from PIL import Image
from pylab import *

server = xmlrpc.client.ServerProxy("http://localhost:8073")


def binarizate_image(image_array, limit):
    pickle_image = pickle.dumps(image_array)
    binary_image = xmlrpc.client.Binary(pickle_image)
    response = server.image_binarization_by_limit(binary_image, limit)
    binarizated_image_array = pickle.loads(response.data)
    return binarizated_image_array


# Монохромное изображение
monochrome_image = Image.open('resources/11.bmp')
monochrome_image_array = array(monochrome_image)
matplotlib.pyplot.imshow(monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

binarizated_monochrome_image_array = binarizate_image(monochrome_image_array, 50)
matplotlib.pyplot.imshow(binarizated_monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

binarizated_monochrome_image_array = binarizate_image(monochrome_image_array, 128)
matplotlib.pyplot.imshow(binarizated_monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

binarizated_monochrome_image_array = binarizate_image(monochrome_image_array, 250)
matplotlib.pyplot.imshow(binarizated_monochrome_image_array, cmap="gray")
matplotlib.pyplot.show()

# Цветное изображение
color_image = Image.open('resources/Jellyfish.jpg')
color_image_array = array(color_image)
matplotlib.pyplot.imshow(color_image, cmap="gray")
matplotlib.pyplot.show()

binarizated_color_image_array = binarizate_image(color_image_array, 50)
matplotlib.pyplot.imshow(binarizated_color_image_array, cmap="gray")
matplotlib.pyplot.show()

binarizated_color_image_array = binarizate_image(color_image_array, 128)
matplotlib.pyplot.imshow(binarizated_color_image_array, cmap="gray")
matplotlib.pyplot.show()

binarizated_color_image_array = binarizate_image(color_image_array, 250)
matplotlib.pyplot.imshow(binarizated_color_image_array, cmap="gray")
matplotlib.pyplot.show()
