from logging import Logger

from PIL import Image
from typing import Tuple, List
from pathlib import Path
import re
import logging


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

        self.logger: Logger = logging.getLogger("base_image")

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        self._location = _location
        self._name_glob = name_glob
        self._all_bands_associated_with_image: List[Tuple[str, str, str, Image.Image]] = list()

    def get_images(self) -> List[Tuple[str, str, str, Image.Image]]:
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
        date: str = extractor.extract_date()
        position: str = extractor.extract_position()
        loaded_image: Image = self._load_image(image_path)
        self._all_bands_associated_with_image.append((position, date, band, loaded_image))

    @staticmethod
    def _load_image(image_path):
        logging.debug(f"loading image: {image_path.absolute()}")
        image = Image.open(image_path)
        return image


class PathExtractor():
    logger: Logger

    def __init__(self, path: Path):
        self.subject: str = str(path.name)
        self.logger: Logger = logging.getLogger("base_image")

    def extract_date(self) -> str:
        self.logger.debug("extracting date")
        return self._extract_pattern("-(\d{4}-\d{2}-\d{2}).png")

    def extract_position(self) -> str:
        self.logger.debug("extracting position")
        return self._extract_pattern("(\d{4}-\d{5})-")

    def extract_band(self) -> str:
        return self._extract_pattern("-(?:(B\d{2})|(TLI))-")

    def _extract_pattern(self, pattern: str) -> str:
        resultant_extraction = re.findall(pattern, self.subject)
        self.logger.info(f"Resultant value: {resultant_extraction}")
        if len(resultant_extraction) == 0:
            self.logger.info(f"The pattern: [{resultant_extraction}] has resulted in 0 results.")
        return resultant_extraction[0]
