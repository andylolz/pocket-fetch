from os import makedirs, getenv
from os.path import exists
from pathlib import Path
import urllib3

from dotenv import load_dotenv
from pycketcasts import PocketCast
from slugify import slugify
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
OUTPUT_PATH = Path('./output')
load_dotenv()


def fetch_in_progress():
    print('Connecting to pocketcast ...')
    pocket = PocketCast(getenv('user'), password=getenv('password'))
    for x in pocket.in_progress:
        print(f'Fetching "{x.title}" ...')
        filepath = OUTPUT_PATH / \
            slugify(x.podcast_title) / \
            slugify(x.podcast_title)
        makedirs(filepath, exist_ok=True)
        filename = slugify(x.title) + ".mp3"
        r = requests.get(x.url, verify=False, stream=True)

        if exists(filepath / filename):
            continue

        with open(filepath / filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)


if __name__ == "__main__":
    fetch_in_progress()
