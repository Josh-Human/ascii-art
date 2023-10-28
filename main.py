import argparse
import math
from PIL import Image

MAX_BRIGHTNESS = 255
CHARACTERS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

parser = argparse.ArgumentParser(description='Print an ascii art version of an image in the console.')
parser.add_argument('path', metavar='p', type=str, nargs='?',
                    help='path of image to transform')
parser.add_argument('--brightness_algorithm', metavar="--b",type=str, required=False, choices=['luminosity', 'min_max', 'average'],
                    default='average',
                    help='algorithm to calculate pixel brightness')

class Pixel:
    def __init__(self, rgb_values=(0,0,0)):
        self.R = rgb_values[0]
        self.G = rgb_values[1]
        self.B = rgb_values[2]

def main(img_path, brightness_algorithm):
    img = Image.open(img_path)

    print("Succesfully loaded image!")

    resalce_factor = 0.25
    img.resize((round(img.width * resalce_factor), round(img.height * resalce_factor)))

    print("Image size: {} x {}".format(img.width, img.height))

    pixel_matrix = construct_empty_matrix(img.height, img.width)
    brightness_matrix = construct_empty_matrix(img.height, img.width)
    character_matrix = construct_empty_matrix(img.height, img.width)

    for y in range(img.height):
        for x in range(img.width):
            pixel_matrix[x][y] = Pixel(img.getpixel((x, y)))

            pixel = pixel_matrix[x][y]

            brightness_matrix[x][y] = calculate_brightness(pixel, brightness_algorithm)
            character_matrix[x][y] = convert_brightness_to_charcter(brightness_matrix[x][y])
            print(character_matrix[x][y], end="")
        print("")


def construct_empty_matrix(height, width):
    return [[None] * height] * width

def convert_brightness_to_charcter(brightness):
    position = round((brightness/ MAX_BRIGHTNESS) * len(CHARACTERS))
    return CHARACTERS[position]

def calculate_brightness(pixel, algo=None):
    if algo == "min_max":
        return round((max(pixel.R, pixel.G, pixel.B) + min(pixel.R, pixel.G , pixel.B)) / 2)
    elif algo == "luminosity":
        return round(0.21 * pixel.R + 0.72 * pixel.G + 0.07 * pixel.B)
    else:
        return round((pixel.R + pixel.G + pixel.B) / 3)




if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    main(args.path, args.brightness_algorithm)