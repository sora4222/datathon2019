from PIL import Image
from typing import Tuple, List
from pathlib import Path
import re


class BaseImageLoader():
    """
    Obtains all the band images related to a single image name within the location folder
    """

    def __init__(self, location: str, name: str):
        """
        BaseImageLoader brings in images as are required.
        :param location: The directory location of the image
        :param name: the starting component of the name, e.g. give 7680-10249 for images
         like 7680-10249-TCI-2016-12-22.png
        """

        assert location is not None and location, "location is empty or 'None'"
        self.location = location
        self.name = name
        self.all_bands_associated_with_image: List[Tuple[str, str, Image]] = list()

    def get_images(self):
        if len(self.all_bands_associated_with_image) == 0:
            self.get_all_bands()

        return self.all_bands_associated_with_image

    def _get_all_bands(self) -> List[Tuple[str, str, Image]]:
        """
        Gets all bands and colour images and adds their information to the internal list
        :return:
        """

        path = Path(self.location)
        all_file_paths = path.glob(self.name_glob)

        file_path: Path
        for file_path in all_file_paths:
            extractor = PathExtractor(file_path)
            band: str = extractor.extract_band()
            date: str = extractor.extract_date()
            position: str = extractor.extract_position()
            loaded_image:Image = self._load_image()
            self.all_bands_associated_with_image.append((position, date, band, loaded_image))

    def _load_image(self):
        image = Image()


class PathExtractor():
    def __init__(self, path: Path):
        self.subject: str = str(path.name)

    def extract_date(self) -> str:
        return self._extract_pattern("-(\d{4}-\d{2}-\d{2}).png")

    def extract_position(self) -> str:
        return self._extract_pattern("(\d{4}-\d{5})-")

    def extract_band(self) -> str:
        return self._extract_pattern("-(?:(B\d{2})|(TLI))-")

    def _extract_pattern(self, pattern: str) -> str:
        resultant_extraction = re.findall(pattern, self.subject)
        assert len(resultant_extraction) == 0
        return resultant_extraction[0]
