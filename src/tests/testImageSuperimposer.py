from PIL import Image
import src.imageprocessing.imageSuperimposer as img_imposer
import pathlib
from src.imageprocessing.imageValue import ImageValue
import datetime

from typing import List

def test_image_max():
    white_image: Image = Image.open(pathlib.Path("resources/whiteimage.png").absolute(), "r")
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.jpg").absolute(), "r")
    assert 255 == img_imposer.ImageNormalizer._min_max_band([white_image, black_image])


def test_image_normalizer():
    white_image: Image = Image.open(pathlib.Path("resources/whiteimage.png").absolute(), "r")
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.jpg").absolute(), "r")

    images: List[ImageValue] = [ImageValue(white_image, "a", datetime.datetime.now(), 'asdf'),
                                ImageValue(white_image, "b", datetime.datetime.now(), "adff")]

    normalizer = img_imposer.ImageNormalizer(images)
    resultant_images = normalizer.normalize()

    assert images == resultant_images
