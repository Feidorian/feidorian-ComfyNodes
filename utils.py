"""
@Author: Feidorian
"""

from contextlib import contextmanager
import io
import sys
import os
from datetime import datetime, timedelta
import torch
import numpy as np
import math
from PIL import Image, ImageOps


@contextmanager
def suppress_output():
    """
    Suppress standard output in code block

    Usage:
        with suppress_output():
            code
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        yield
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


ANY_TYPE = AnyType("*")


def generate_mappings(mappings):
    NODE_CLASS_MAPPINGS = [(item["name"], item["function"]) for item in mappings]
    NODE_DISPLAY_NAME_MAPPINGS = [
        (item["name"], item["display_name"]) for item in mappings
    ]
    return {
        "NODE_CLASS_MAPPINGS": NODE_CLASS_MAPPINGS,
        "NODE_DISPLAY_NAME_MAPPINGS": NODE_DISPLAY_NAME_MAPPINGS,
    }


def is_valid_image(dir: str, filename:str) -> bool:
    path = os.path.join(dir, filename)
    try:
        img = Image.open(path)
        img.verify()
        Image.close()
        return True
    except:
        return False


def get_comfy_image_mask(image_path: str) -> tuple[Image.Image, Image.Image]:
    i = Image.open(image_path)
    i = ImageOps.exif_transpose(i)
    image = i.convert("RGB")
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]
    if "A" in i.getbands():
        mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
        mask = 1.0 - torch.from_numpy(mask)
    else:
        mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

    return (image, mask)



class EllapsedTracker:
    def __init__(self):
        self.approx_time = None
        self.current_start_time = None

    def log_start(self):
        self.current_start_time = datetime.now()

    def log_end(self):
        if self.current_start_time:
            time = datetime.now()
            approx_time = (time - self.current_start_time).total_seconds()
            # if self.approx_time: self.approx_time = math.ceil((self.approx_time + approx_time)/2)
            # else:
            self.approx_time = math.ceil(approx_time)

    def get_ellapsed(self):
        return self.approx_time


ellapsed_tracker = EllapsedTracker()
