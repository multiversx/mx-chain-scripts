import shutil
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from rich import print

from multistage.constants import TEMPORARY_DIRECTORIES_PREFIX


def fetch_archive(archive_url: str, destination_path: Path):
    archive_url_parsed = urlparse(archive_url)
    file_name = Path(archive_url_parsed.path).name

    with tempfile.TemporaryDirectory(prefix=TEMPORARY_DIRECTORIES_PREFIX) as tmpdirname:
        download_path = Path(tmpdirname) / file_name
        extraction_path = Path(tmpdirname) / "extracted"

        print(f"Downloading archive {archive_url} to {download_path} ...")
        urllib.request.urlretrieve(archive_url, download_path)

        print(f"Unpacking archive {download_path} to {extraction_path} ...")
        shutil.unpack_archive(download_path, extraction_path)

        items = list(extraction_path.glob("*"))
        assert len(items) == 1, "archive should have contained only one top-level item"
        top_level_item = items[0]

        print(f"Moving {top_level_item} to {destination_path} ...")
        shutil.move(top_level_item, destination_path)
