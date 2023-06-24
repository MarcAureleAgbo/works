import pandas as pd
import requests

def download_data(url, file_path):
    """
    Download data from URL and save to file_path
    """
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    url = "https://example.com/air_liquid_data.csv"
    file_path = "../data/air_liquid_data.csv"
    download_data(url, file_path)
