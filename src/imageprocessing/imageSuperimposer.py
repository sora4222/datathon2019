import numpy as np
from matplotlib import cm
from typing import Generator, List
from functools import reduce

from PIL import Image
import cv2

from src.imageprocessing.imageValue import ImageValue


class ImageSuperimposer():
    def __init__(self, base_image: Image.Image):
        self._base_image: np.ndarray = self.convert_to_opencv(base_image)
        self._cm_hot = cm.get_cmap("hot")

    def superimpose(self, image_for_colormap: Image.Image) -> np.ndarray:
        """
        Will take the given image_arr and use it as a heat map on the base image_arr

        :param image_for_colormap: the image_arr in PIL format that is used as a heat map
        :return: An Open CV image_arr (np.ndarray)
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


class ImageNormalizer():
    """
    Processes the images to be relative to each other. This allows the heat-maps to be
    better visible for the viewer.
    """

    def __init__(self, image_list: List[ImageValue], black_already: bool = False):
        """

        :param image_list: A list of the images, it expects the image to be based on PIL
        :param black_already: A boolean that is set to true if the image has been passed in as
        a numpy array converted to black and white.
        """
        self.images: List[ImageValue]
        if black_already:
            self.images = image_list
        elif type(image_list[0].image) is np.ndarray:
            self.images = [ImageValue.fromimage(image_val, cv2.cvtColor(image_val.image, cv2.COLOR_BGRA2GRAY))
                           for image_val in image_list]
        else:
            self.images = [ImageValue.fromimage(image_val, cv2.cvtColor(np.array(image_val.image), cv2.COLOR_BGRA2GRAY))
                           for image_val in image_list]

    def normalize(self) -> List[ImageValue]:
        max_value_in_image: int = self._max_band()
        min_value_in_image: int = self._min_band()

        multiplier: int = self._multiplier_to_peak(max_value_in_image)
        return self._normalize_each_image(multiplier, min_value_in_image)

    def _max_band(self) -> int:
        flattened_images_bw: Generator[np.ndarray] = self._flatten_images()
        return reduce(lambda state, image_arr: max(np.max(image_arr), int(state)), flattened_images_bw, 0)

    def _min_band(self) -> int:
        flattened_images_bw: Generator[np.ndarray] = self._flatten_images()
        return reduce(lambda state, image_arr: min(np.min(image_arr), int(state)), flattened_images_bw, 0)

    def _flatten_images(self):
        numpy_images_bw: Generator[np.ndarray] = (image.image
                                                  for image in self.images)
        flattened_images_bw: Generator[np.ndarray] = (image_arr.flatten() for image_arr in numpy_images_bw)
        return flattened_images_bw

    def _multiplier_to_peak(self, max_number: int) -> int:
        return 0 if max_number == 0 else int(255.0 / max_number)

    def _normalize_each_image(self, multiplier: int, gamma: int) -> List[ImageValue]:
        image: ImageValue
        scaled_images: List[ImageValue] = []
        for image in self.images:
            scaled_images.append(ImageValue.fromimage(image, multiplier * image.image - gamma))

        return scaled_images
