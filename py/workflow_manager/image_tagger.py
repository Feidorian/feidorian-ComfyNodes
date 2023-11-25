import math
import random
import torch
import random
import os
from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
from itertools import repeat
import numpy as np
import json
from datetime import datetime, timedelta
from ...log import log
from ...utils import is_valid_image, get_comfy_image_mask


class ImageTagger:
    PRODUCT_TAG = "product_"
    PROCESSED_TAG = "processed_"

    curr_orig_filename = None
    curr_orig_ext = None
    curr_dir = None
    curr_processed_filename = None
    curr_product_filename = None

    start_time = None
    processed_file_count = 0
    unprocessed_file_count = 0

    @staticmethod
    def random_picker(images: list[str]) -> str:
        return random.choice(images)

    @staticmethod
    def linear_picker(images: list[str]) -> str:
        return images[0]

    def process_file(self, dir: str, file: str):
        filename, ext = [(t[0], t[1].strip(".")) for t in [os.path.splitext(file)]][0]
        self.curr_dir = dir
        self.curr_orig_filename = filename
        self.curr_orig_ext = ext
        self.curr_processed_filename = f"{self.PROCESSED_TAG}{self.curr_orig_filename}"
        self.curr_product_filename = f"{self.PRODUCT_TAG}{self.curr_orig_filename}"
        new_filename = f"{self.curr_processed_filename}.{self.curr_orig_ext}"
        old_file = os.path.join(dir, file)
        new_file = os.path.join(dir, new_filename)
        os.rename(old_file, new_file)

    def fix_errors(self, dir: str, files: list[str]):
        processed_files = [file for file in files if self.PROCESSED_TAG in file]
        self.processed_file_count = len(processed_files)
        product_files = [file for file in files if self.PRODUCT_TAG in file]
        self.unprocessed_file_count = len(
            [file for file in files if file not in processed_files + product_file]
        )
        for processed_file in processed_files:
            is_valid = False
            p1 = processed_file.replace(self.PROCESSED_TAG, "")
            for product_file in product_files:
                p2 = product_file.replace(self.PRODUCT_TAG, "")
                if p1 == p2:
                    is_valid = True
                    break
            if not is_valid:
                old_file = os.path.join(dir, processed_file)
                new_file = os.path.join(dir, p1)
                os.rename(old_file, new_file)
                self.processed_file_count -= 1
                self.unprocessed_file_count += 1

    def set_start_time(self):
        self.start_time = datetime.now()

    def __reset__(self):
        self.start_time = None
        self.processed_file_count = 0
        self.unprocessed_file_count = 0

    def log_time(self):
        if not self.start_time:
            return
        self.processed_file_count += 1
        self.unprocessed_file_count -= 1
        current_time = datetime.now()
        approx_time = math.ceil((current_time - self.start_time).total_seconds())
        remaining_time = seconds = self.unprocessed_file_count * approx_time
        log.info("**** Workflow Image Manager Status ****")
        log.info(f"Number of Tasks Completed: {self.processed_file_count}")
        log.info(f"Number of Tasks Left: {self.unprocessed_file_count}")
        log.info(f"Previous Completion Time: {timedelta(seconds=approx_time)}")
        log.info(f"Remaining Time (Estimate): {timedelta(seconds=remaining_time)}")
        self.__reset__()


tagger = ImageTagger()


class WorkflowImageLoader:
    SELECTION_MODE = {
        "linear": ImageTagger.linear_picker,
        "random": ImageTagger.random_picker,
    }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    CATEGORY = "feidorian/workflow-manager"
    FUNCTION = "ImageLoader"

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return float("nan")

    @classmethod
    def INPUT_TYPES(cls):
        selection_mode = list(cls.SELECTION_MODE.keys())
        return {
            "required": {
                "directory": ("STRING", {"placeholder": "Image Directory"}),
                "selection_mode": (
                    selection_mode,
                    {"default": "random"},
                ),
            }
        }

    def ImageLoader(self, directory, selection_mode):
        tagger.set_start_time()

        if not os.path.exists(directory):
            raise Exception(f"Directory {directory} does not Exist.")

        image_files = [
            file for file in os.listdir(directory) if is_valid_image(directory, file)
        ]

        tagger.fix_errors(directory, image_files)

        image_files = [
            file
            for file in image_files
            if tagger.PROCESSED_TAG not in file and tagger.PRODUCT_TAG not in file
        ]

        if len(image_files) == 0:
            raise Exception(f"No Unprocessed File Found in directory {directory}!")

        chosen_image = self.SELECTION_MODE(selection_mode)(image_files)
        chosen_image_path = os.path.join(directory, chosen_image)
        tagger.process_file(directory, chosen_image)
        return get_comfy_image_mask(chosen_image_path)


class WorkflowImageSaver:
    CATEGORY = "feidorian/workflow-manager"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "ImageSaver"
    type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Images": ("IMAGE",),
                "with_workflow": ("BOOLEAN", {"default": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def ImageSaver(self, Images, with_workflow, prompt=None, extra_pnginfo=None):
        path = tagger.curr_dir
        results = list()
        if not path:
            raise Exception("Missing Path. Path must be provided to loader node.")
        filename = tagger.curr_product_filename

        for index in range(len(Images)):
            image = Images[index]
            if index > 0:
                filename = f"{filename}_{index:05d}"
            image = 255.0 * image.cpu().numpy()
            image = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
            if with_workflow:
                metadata = PngInfo()
                if prompt:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo:
                    for x in extra_pnginfo:
                        metadata.add(x, json.dumps(extra_pnginfo[x]))
            curr_filename = f"{filename}.png"
            image.save(
                os.path.join(path, curr_filename),
                pnginfo=metadata,
                compress_level=4,
            )
            results.append(
                {"filename": curr_filename, "subfolder": "", "type": self.type}
            )
        tagger.log_time()
        return {"ui": {"images": results}}
