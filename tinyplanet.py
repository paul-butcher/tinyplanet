from __future__ import division

import math
from PIL import Image, ImageDraw, ImageFilter
#
# def find_horizon_ends(im):
#     q_image = im.filter(ImageFilter.BoxBlur(5)).quantize(colors=5)
#     q_image.save('q.png')
#     imgX, imgY = im.size
#     lhs_changes = find_changes(q_image, imgY,  0)
#     print lhs_changes
#     rhs_changes = find_changes(q_image, imgY, imgX - 1)
#     print rhs_changes
#
# def find_changes(im, imgY, column):
#     changes = []
#     prev_pixel = im.getpixel((column, 0))
#     for y in range(1, imgY):
#         current_pixel = im.getpixel((column, y))
#         if current_pixel != prev_pixel:
#             changes.append((y, prev_pixel, current_pixel))
#             prev_pixel = current_pixel
#     return changes


# image size
linear_image = Image.open("/Users/butchp01/Downloads/IMG_20180620_130630.jpg")

# lhs = 200
# rhs = 140
lhs = 2000
rhs = 1400

imgY = linear_image.height
imgY = int(imgY / 10)
linear_image = linear_image.resize((imgY, imgY))
lhs /=10
rhs /=10
# find_horizon_ends(linear_image)

#linear_image = linear_image.transpose(Image.FLIP_TOP_BOTTOM)
imgX, imgY = linear_image.size

print 'squared %sx%s' % (imgX, imgY)
linear_image.save('square.png')

def straighten_horizon(im, lhs, rhs):
    """
    Straighten the horizon of the image by skewing either end towards the centre of the
    difference between the two
    :param im: A PIL image
    :param lhs: Horizon at the left-hand end
    :param rhs: Horizon at the right hand end
    :return:
    """
    diff = (lhs - rhs) / 2
    imgX, imgY = im.size

    a = (diff/(imgX/2)) * -1

    def yoffset(x):
        """
        linear function - f(x) = ax + b
        """
        return int((a * x) + diff)

    for y in range(0, imgY):
        for x in range(0, imgX//2):
            #dy = (diff - x)
            dy = yoffset(x)
            try:
                im.putpixel((x, y),
                    im.getpixel((x, y + dy))
                )
                im.putpixel((imgX - x, imgY - y),
                    im.getpixel((imgX - x, imgY - y - dy))
                )
            except IndexError:
                pass
    im.save('straight.png')
    return im


linear_image = straighten_horizon(linear_image, lhs, rhs)

# find_horizon_ends(linear_image)


linear_image = linear_image.transpose(Image.FLIP_TOP_BOTTOM)


circle_image = Image.new("RGB", (imgX, imgY))

# rectangle to polar coordinates
maxradius = imgX / 2 #math.sqrt(imgX**2 + imgY**2)/2
rscale = imgX / maxradius
tscale = imgY / (2*math.pi)

for y in range(0, imgY):
    dy = y - imgY/2

    for x in range(0, imgX):
        dx = x - imgX/2
        t = math.atan2(dy,dx)%(2*math.pi)*tscale
        r = math.sqrt(dx**2+dy**2)*rscale

        if 0<= t < imgX and 0 <= r < imgY:
            circle_image.putpixel((x, y), linear_image.getpixel((t, r)))

circle_image.save("polar.png", "PNG")