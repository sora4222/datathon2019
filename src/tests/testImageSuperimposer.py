from src.imageprocessing.ImageSuperimposer import ImageSuperimposer
from PIL import Image
import matplotlib.cm as cm
def test_manual_image_superimposed():
    base_image = Image.open("C:\\Users\\sora4\\PycharmProjects\\datathon2019\\phase-01\\data\\sentinel-2a-tile-7680x-10240y\\timeseries\\7680-10240-TCI-2016-12-22.png")
    superImposer = ImageSuperimposer(base_image)

    map_image = Image.open(
        "C:\\Users\\sora4\\PycharmProjects\\datathon2019\\phase-01\\data\\sentinel-2a-tile-7680x-10240y\\timeseries\\7680-10240-TCI-2016-12-22.png")
    image_back = superImposer.superimpose(map_image)

    image_back.show()