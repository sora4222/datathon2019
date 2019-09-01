from PIL import Image

class ImageValue():
    """
    Holds the image and it's defining properties.
    """
    def __init__(self, image: Image, position: str, date: str, band: str):
        """
        Used to contain the image and it's defining properties.
        :param image: Image of farm
        :param position: Position of image
        :param date: Date the image was taken
        :param band: The light band that was used for the image
        """
        self.image: Image = image
        self.position: str = position
        self.date: str = date
        self.band: band = band

    def __str__(self):
        return f"position: {self.position}, band: {self.band}, " \
               f"date: {self.date}, image present: {self.image is not None}"

    def get_image(self) -> Image:
        return self.image