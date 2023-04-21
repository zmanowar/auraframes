import os
import shutil
from datetime import datetime
from io import BytesIO
from loguru import logger
from PIL import Image, UnidentifiedImageError
import httpx

from auraframes.exif import ExifWriter
from auraframes.models.asset import Asset
from auraframes.utils import settings


def _get_path_safe_datetime(date_str: datetime):
    return date_str.strftime('%Y%m%dT%H%M%S')


def get_thumbnail(asset: Asset, original_image: BytesIO = None):
    """
    Aura thumbnails can be saved incorrectly, we can generate our own if we have the original image.
    TODO: We could also check the other fields on `Asset` to see if there are smaller images instead of using PIL.
    """
    thumbnail_response = httpx.get(asset.thumbnail_url)
    thumbnail_bytes = BytesIO(thumbnail_response.content)
    try:
        with Image.open(thumbnail_bytes) as http_thumbnail:
            http_thumbnail.verify()
    except UnidentifiedImageError:
        if not original_image:
            return None

        with Image.open(original_image) as pil_image:
            out_bytes = BytesIO()
            pil_image.thumbnail((100, 100))
            pil_image.save(out_bytes, 'jpeg')
            return out_bytes.getvalue()

    return thumbnail_bytes.getvalue()


def get_image_from_asset(asset: Asset, path: str, exif_writer: ExifWriter = None, ignore_cache=False):
    new_filename = os.path.join(path, f'{_get_path_safe_datetime(asset.taken_at_dt)}-{asset.file_name}')
    if (os.path.isfile(new_filename) and not ignore_cache):
        with open(new_filename, 'rb') as in_file:
            return in_file.read()
    original_image_bytes = httpx.get(f'{settings.IMAGE_PROXY_BASE_URL}/{asset.user_id}/{asset.file_name}').content

    thumbnail = get_thumbnail(asset, BytesIO(original_image_bytes)) if exif_writer else None
    image = exif_writer.write_exif(original_image_bytes, asset, thumbnail)

    with open(new_filename, 'wb') as out:
        shutil.copyfileobj(image, out)
    return original_image_bytes
