import requests
import gzip
import shutil
import os

url = "http://data.phishtank.com/data/online-valid.csv.gz"

output_gz = "data/raw/phishtank_urls.csv.gz"
output_csv = "data/raw/phishtank_urls.csv"

headers = {
    "User-Agent": "phishtank/peg-ai-research"
}

response = requests.get(url, headers=headers, stream=True)

with open(output_gz, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("Download complete")

with gzip.open(output_gz, "rb") as f_in:
    with open(output_csv, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("File extracted successfully")