from pathlib import Path
from src.imageprocessing.baseImageBuilder import PathExtractor

def test_image_extractor_extracts_dates():
    extractor = PathExtractor(Path("7680-10240-B01-2017-01-01.png"))
    assert extractor.extract_date().strftime("%Y-%m-%d") == "2017-01-01"

def test_image_extractor_extracts_bands():
    extractor = PathExtractor(Path("7680-10240-B01-2017-01-01.png"))
    assert extractor.extract_band() == "B01"