# -*- coding: utf-8 -*-

def combine_vs(first_img, second_img):
    import requests
    first_img = requests.get(first_img, stream=True)
    second_img = requests.get(second_img, stream=True)

    from PIL import Image
    from io import BytesIO

    images = [Image.open(BytesIO(first_img.content)), Image.open(BytesIO(second_img.content))]
    widths, heights = zip(*(i.size for i in images))

    max_height = sum(heights)
    max_width = int(max_height/3 * 2)

    new_img = Image.new('RGB', (max_width, max_height), '#070707')

    new_img.getcolors()

    y_offset = 0
    for idx, im in enumerate(images):
        new_img.paste(im, (int((max_width - widths[idx]) / 2), y_offset), im)
        y_offset += im.size[0]

    return new_img