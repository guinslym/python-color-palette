from colorthief import ColorThief
import webcolors

color_thief = ColorThief('a.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=6)

print(webcolors.rgb_to_hex(dominant_color))
palette = [webcolors.rgb_to_hex(color) for color in palette]
print(palette)

import math
def distance(color1, color2):
    return math.sqrt(sum([(e1-e2)**2 for e1, e2 in zip(color1, color2)]))


def best_match(sample, colors):
    by_distance = sorted(colors, key=lambda c: distance(c, sample))
    return by_distance[0:5]

colors = [

(0, 0, 0),
(0, 0, 170),
(0, 170, 0),
(0, 170, 170),
(170, 0, 0),
(170, 0, 170),
(255, 170, 0),
(170, 170, 170),
(85, 85, 85),
(85, 85, 255),
(85, 255, 85),
(85, 255, 255),
(255, 85, 85),
(255, 85, 255),
(255, 255, 85),
(255, 255, 255)

]


result = best_match((60,43,44), colors)
palette = [webcolors.rgb_to_hex(color) for color in result]
print(palette)

from flask_sqlalchemy import SQLAlchemy
