"""
post gen script to download unsplash details and update
configuration files
"""

import os
from pathlib import Path
from urllib.request import urlretrieve

from ruamel.yaml import YAML
from unsplash.api import Api
from unsplash.auth import Auth
from unsplash.models import Photo


def get_yaml(file_path: str) -> dict:
    yaml = YAML(typ="safe")
    with open(file_path, "rb") as doc:
        data = yaml.load(doc)
    return data


def write_yaml(file_path: str, content: dict) -> None:
    yaml = YAML()
    yaml.default_flow_style = False

    with open(file_path, "wb") as f:
        yaml.dump(content, f)


class UnsplashApi:
    def __init__(self, unsplash_client_id: str):
        # can just use the public access, no need for secret
        auth = Auth(unsplash_client_id, "", "", "")
        self.api = Api(auth)
        self.photo_cache = {}

    def get_photo(self, url: str) -> Photo:
        unsplash_id = url.split("/")[-1]
        return self.api.photo.get(unsplash_id)

    def download_photo_from_url(self, url: str, dest: Path) -> None:
        photo = self.photo_cache.get(url, self.get_photo(url))
        self.photo_cache[url] = photo
        urlretrieve(photo.urls.raw, dest)

    def get_info_on_photo(self, url: str) -> dict:
        """
        get a dictionary of information
        """

        photo = self.get_photo(url)
        return {
            "unsplash_id": photo.id,
            "alt_text": photo.alt_description,
            "source_url": photo.links.html,
            "credit": f"[Photo by {photo.user.name}]({photo.links.html}) on Unsplash",
            "description": photo.description,
        }


def update_document_from_unsplash(doc_folder: Path):
    doc_yaml = get_yaml(doc_folder / "settings.yaml")
    if "unsplash_title_image_url" not in doc_yaml:
        return

    unsplash_url = doc_yaml["unsplash_title_image_url"]
    api = UnsplashApi(os.environ["UNSPLASH_CLIENT_ID"])
    details = api.get_info_on_photo(unsplash_url)
    api.download_photo_from_url(
        unsplash_url, doc_folder / f"{details['unsplash_id']}.jpg"
    )
    doc_yaml["header"]["location"] = f"{details['unsplash_id']}.jpg"
    doc_yaml["header"].update(details)
    write_yaml(doc_folder / "settings.yaml", doc_yaml)
    (doc_folder / "default-header-image.jpg").unlink()


if os.environ.get("UNSPLASH_CLIENT_ID", None) is not None:
    # this file runs with the content in the current directory
    try:
        update_document_from_unsplash(Path("."))
    except Exception as e:
        print(f"Error updating document: {e}")
else:
    print("No UNSPLASH_CLIENT_ID env variable.")
