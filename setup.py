import requests
from tqdm import tqdm
import zipfile
from os import remove

file_url = "https://sora4222.com/files/phase-01-rev1.12.zip"

response = requests.get(file_url, stream=True)

with open("temp.zip", "wb") as handle:
    for data in tqdm(response.iter_content()):
        handle.write(data)

with zipfile.ZipFile("temp.zip", "r") as zip_file:
    zip_file.extractall()

remove("temp.zip")
