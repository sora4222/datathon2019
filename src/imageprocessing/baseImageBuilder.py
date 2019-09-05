from logging import Logger

from PIL import Image
from typing import Tuple, List
from pathlib import Path
import re
import logging
from src.imageprocessing.imageValue import ImageValue
import datetime

class BaseImageLoader():
    """
    Obtains all the band images related to a single image name within the _location folder
    """

    def __init__(self, _location: str, name_glob: str):
        """
        BaseImageLoader brings in images as are required.
        :param _location: The directory _location of the image
        :param name_glob: name glob of the images to load.
        """

        assert _location is not None and _location, "_location is empty or 'None'"

        self.logger: Logger = logging.getLogger("_base_image")

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        self._location = _location
        self._name_glob = name_glob
        self._all_bands_associated_with_image: List[ImageValue] = list()

    def get_images(self) -> List[ImageValue]:
        """
        Gets the position, date, band, and the images for the subjectImage given
        :return: position, date, band, and the images
        """
        if len(self._all_bands_associated_with_image) == 0:
            self._get_all_bands()

        return self._all_bands_associated_with_image

    def _get_all_bands(self):
        """
        Gets the position, date, band, and the images and adds their information to the internal list
        :return:
        """

        path = Path(self._location)
        all_file_paths = path.glob(self._name_glob)

        image_path: Path
        for image_path in all_file_paths:
            self.logger.debug(f"image_path {image_path}")
            self._extract_information_of_image(image_path)

    def _extract_information_of_image(self, image_path):
        extractor = PathExtractor(image_path)
        band: str = extractor.extract_band()
        date: datetime.datetime = extractor.extract_date()
        position: str = extractor.extract_position()
        loaded_image: Image = self._load_image(image_path)
        self._all_bands_associated_with_image.append(ImageValue(loaded_image, position, date, band))

    @staticmethod
    def _load_image(image_path):
        logging.debug(f"loading image: {image_path.absolute()}")
        image_loaded: Image = Image.open(image_path)
        image = image_loaded.convert("RGB")
        return image


class PathExtractor():
    logger: Logger

    def __init__(self, path: Path):
        self.subjectImage: str = str(path.name)
        self.logger: Logger = logging.getLogger("_base_image")

    def extract_date(self) -> datetime.datetime:
        self.logger.debug("extracting date")
        date = self._extract_pattern("-(\d{4}-\d{2}-\d{2}).png")
        return datetime.datetime.strptime(date, "%Y-%m-%d")

    def extract_position(self) -> str:
        self.logger.debug("extracting position")
        return self._extract_pattern("(\d{4}-\d{5})-")

    def extract_band(self) -> str:
        self.logger.debug("extracting band")
        return self._extract_pattern("-(?:(B\d{1,2}\w?)|(T[LC]I))-")

    def _extract_pattern(self, pattern: str) -> str:
        resultant_extraction = re.findall(pattern, self.subjectImage)

        self.logger.debug(f"Resultant value: {resultant_extraction}")
        if not isinstance(resultant_extraction[0], str):
            return self.remove_empty_strings(resultant_extraction)[0]
        else:
            return resultant_extraction[0]

    @staticmethod
    def remove_empty_strings(resultant_extraction) -> List[str]:
        return list(filter(None, resultant_extraction[0]))
