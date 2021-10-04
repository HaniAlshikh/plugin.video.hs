# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO


def combine_vs(first_img, second_img, banner=False):
    import requests
    first_img = requests.get(first_img, stream=True)
    second_img = requests.get(second_img, stream=True)

    images = [Image.open(BytesIO(first_img.content)), Image.open(BytesIO(second_img.content))]
    widths, heights = zip(*(i.size for i in images))

    if banner:
        return _combine_vs_banner(images, widths, heights)

    return _combine_vs_poster(images, widths, heights)


def _combine_vs_poster(images, widths, heights):
    max_height = sum(heights)
    padding = int(max_height * 0.1)
    max_height += padding
    max_width = int(max_height/3 * 2)  # Poster 3:2

    new_img = Image.new('RGB', (max_width, max_height), '#070707')

    y_offset = 0
    for idx, im in enumerate(images):
        new_img.paste(im, (int((max_width - widths[idx]) / 2), y_offset), im.convert("RGBA"))
        y_offset += im.size[0] + padding

    return new_img


def _combine_vs_banner(images, widths, heights):
    max_width = sum(widths)
    padding = int(max_width * 0.1)
    max_width += padding * (len(images) + 1)
    max_height = int(7 * (max_width / 8))  # banner 7:8

    new_img = Image.new('RGB', (max_width, max_height), '#070707')

    x_offset = padding
    for idx, im in enumerate(images):
        new_img.paste(im, (x_offset, int((max_height - heights[idx]) / 2)), im.convert("RGBA"))
        x_offset += im.size[0] + padding

    return new_img
