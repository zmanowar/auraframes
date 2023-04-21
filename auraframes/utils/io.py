import json
import os
from typing import Union

from pydantic import BaseModel
from pydantic.json import pydantic_encoder


def build_path(*args, make_dir: bool = True):
    path = os.path.join(*args)
    if make_dir:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def write_model(model: Union[BaseModel, list[BaseModel]], path: str):
    with open(path, 'w') as out:
        json.dump(model, out, default=pydantic_encoder)
