import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from typing import Generator, List

from PIL import Image
import cv2


class ImageSuperimposer():
    def __init__(self, base_image: Image):
        self._base_image: np.ndarray = self.convert_to_opencv(base_image)
        self._cm_hot = cm.get_cmap("hot")

    def superimpose(self, image_for_colormap: Image) -> np.ndarray:
        """
        Will take the given image and use it as a heat map on the base image

        :param image_for_colormap: the image in PIL format that is used as a heat map
        :return: An Open CV image (np.ndarray)
        """
        open_cv_image = self.convert_to_opencv(image_for_colormap)

        heatmap = self._create_colormap_image(open_cv_image)

        return cv2.addWeighted(heatmap, 0.75, self._base_image, 0.25, 0)

    @staticmethod
    def convert_to_opencv(image_for_conversion):
        numpy_image = np.array(image_for_conversion)
        open_cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        return open_cv_image

    def _create_colormap_image(self, open_cv_image):
        grayed_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(grayed_image, cv2.COLORMAP_JET)
        return heatmap

    def superimpose_return_pil_image(self, image_for_colormap: Image) -> Image:
        numpy_superimposed_image = self.superimpose(image_for_colormap)
        return Image.fromarray(cv2.cvtColor(numpy_superimposed_image, cv2.COLOR_BGR2RGB))


def minMaxBand(list_of_band_images: List[Image]):
    numpy_images: Generator[np.ndarray] = (np.array(image) for image in list_of_band_images)
    numpy_images_bw: Generator[np.ndarray] = (cv2.cvtColo)
