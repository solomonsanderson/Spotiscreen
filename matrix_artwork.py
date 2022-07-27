'''Code to open an image and draw it on an rgb led matrix'''


from PIL import Image 
from PIL import ImageDraw
import time 
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def main():
    image = Image.open("album_art.png")
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
# 
    # matrix = RGBMatrix(options = options)
# 
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

    matrix.SetImage(image.convert("RGB"))

    try:
        print("Press CTRL-C to stop.")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        #sys.exit(0)
        pass
if __name__ == "__main__":
    main()