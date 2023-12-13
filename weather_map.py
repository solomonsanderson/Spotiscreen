''' code to draw a 32x32 image showing where it is raining in the UK
The get_weather.py file has code for requesting the weather from an API given the location 
'''



import cv2
import get_weather as gw

map_img = cv2.imread("map.png")
resized = cv2.resize(map_img, (32,32))
dark_blue = [0, 57, 245]
light_blue = [0, 184, 245]

rgb_color = light_blue
rgb_color.reverse()

resized[16, 16] = rgb_color
cv2.imwrite("resized_map.png", resized)

gw.get_weather("50.9105, -1.4049")