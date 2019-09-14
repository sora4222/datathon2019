from PIL import Image
import src.imageprocessing.imageSuperimposer as img_imposer
import pathlib
from src.imageprocessing.imageValue import ImageValue
import datetime
import numpy as np
from typing import List
import cv2


def test_image_normalizer():
    white_image: Image = Image.open(pathlib.Path("resources/whiteimage.png").absolute(), "r")
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.png").absolute(), "r")

    max_in_black = np.amax(np.array(black_image))
    print(f"Before black: {max_in_black}")

    images: List[ImageValue] = [ImageValue(black_image, "a", datetime.datetime.now(), 'asdf'),
                                ImageValue(white_image, "b", datetime.datetime.now(), "adff")]

    normalizer = img_imposer.ImageNormalizer(images)
    resultant_images = normalizer.normalize()
    print(f"Resultant black{np.amax(resultant_images[0].image)}")
    print(f"Resultant white{np.amax(resultant_images[0].image)}")

    assert np.all(resultant_images[0].image == 0)
    assert np.all(resultant_images[1].image == 255)


def test_image_normalizer_black_only():
    black_image: Image = Image.open(pathlib.Path("resources/blackimage.png").absolute(), "r")
    print(np.max(cv2.cvtColor(np.array(black_image), cv2.COLOR_BGRA2GRAY)))
    max_in_black = np.amax(np.array(black_image))
    print(f"Before black: {max_in_black}")

    images: List[ImageValue] = [ImageValue(black_image, "a", datetime.datetime.now(), 'asdf')]

    normalizer = img_imposer.ImageNormalizer(images)
    resultant_images = normalizer.normalize()
    print(f"Resultant black{np.amax(resultant_images[0].image)}")

    assert 0 == np.max(resultant_images[0].image)
