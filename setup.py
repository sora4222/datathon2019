import zipfile
from os import remove
import urllib.request

file_url = "https://sora4222.com/files/phase-01-rev1.12.zip"

print("Downloading file")
urllib.request.urlretrieve(file_url, "temp.zip")

with zipfile.ZipFile("temp.zip", "r") as zip_file:
    zip_file.extractall()

remove("temp.zip")
