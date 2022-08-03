'''Code to open an image and draw it on an rgb led matrix'''


from PIL import Image 
from PIL import ImageDraw
import time 
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def display_image(location):
    image = Image.open(location)
    
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    
    matrix = RGBMatrix(options = options)
    
    image.thumbnail((matrix.width, matrix.height))
    
    matrix.SetImage(image.convert("RGB"))
    
if __name__ == "__main__":
    pass