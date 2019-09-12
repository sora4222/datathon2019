from PIL import Image
from datetime import datetime
import numpy as np
from typing import Union


class ImageValue():
    """
    Holds the image and it's defining properties.
    """

    def __init__(self, image: Union[Image.Image, np.ndarray], position: str, date: datetime, band: str):
        """
        Used to contain the image and it's defining properties.
        :param image: Image of farm
        :param position: Position of image
        :param date: Date the image was taken
        :param band: The light band that was used for the image
        """
        self.image: Union[Image, np.ndarray] = image
        self.position: str = position
        self.date: datetime = date
        self.band: band = band

    @classmethod
    def fromimage(cls, previous_image_value, image_converted: Union[np.ndarray, Image.Image]):
        return cls(image=image_converted,
                   position=previous_image_value.position,
                   date=previous_image_value.date,
                   band=previous_image_value.band)

    def __str__(self):
        return f"position: {self.position}, band: {self.band}, " \
               f"date: {self.date.strftime('%Y-%m-%d')}, image present: {'no' if self.image is None else 'yes'}"

    def get_image(self) -> Image.Image:
        return self.image
