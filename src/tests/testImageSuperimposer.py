from PIL import Image
import src.imageprocessing.imageSuperimposer as img_imposer
import pathlib
from src.imageprocessing.imageValue import ImageValue
import datetime
import numpy as np
from typing import List
import cv2

def test_image_max():
    white_image: Image = Image.open(pathlib.Path("resources/whiteimage.png").absolute(), "r")
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.jpg").absolute(), "r")
    assert 255 == img_imposer.ImageNormalizer._min_max_band([white_image, black_image])


def test_image_normalizer():
    white_image: Image = Image.open(pathlib.Path("resources/whiteimage.png").absolute(), "r")
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.jpg").absolute(), "r")

    max_in_black = np.amax(np.array(black_image))
    print(f"Before black: {max_in_black}")

    images: List[ImageValue] = [ImageValue(black_image, "a", datetime.datetime.now(), 'asdf'),
                                ImageValue(white_image, "b", datetime.datetime.now(), "adff")]

    normalizer = img_imposer.ImageNormalizer(images)
    resultant_images = normalizer.normalize()
    print(f"Resultant black{np.amax(resultant_images[0].image)}")
    print(f"Resultant white{np.amax(resultant_images[0].image)}")

    assert np.amax(np.array(black_image)) == np.max(resultant_images[0].image)
