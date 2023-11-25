import math
import random
import torch
import random
import os
from PIL import Image, ImageOps, ExifTags
from PIL.PngImagePlugin import PngInfo
from itertools import repeat
import numpy as np
import json
import sys
from datetime import datetime, timedelta
from ...log import log
from ...utils import is_valid_image
import folder_paths




def get_comfy_image_mask(image_path: str) -> tuple[Image.Image, Image.Image, str]:
    i = Image.open(image_path)
    
    prompt_text = i.info["prompt_text"] if "prompt_text" in i.info.keys() else ""

    i = ImageOps.exif_transpose(i)
    image = i.convert("RGB")
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]
    if "A" in i.getbands():
        mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
        mask = 1.0 - torch.from_numpy(mask)
    else:
        mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

    return (image, mask.unsqueeze(0), prompt_text)


class ImageTagger:
    PRODUCT_TAG = "product_"
    PROCESSED_TAG = "processed_"

    curr_orig_filename = None
    curr_orig_ext = None
    curr_dir = None
    curr_sub_dir = None
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
        validation_files = processed_files + product_files
        self.unprocessed_file_count = len(
            [file for file in files if file not in validation_files]
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
        remaining_time = self.unprocessed_file_count * approx_time
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

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "prompt_text")
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
                "sub_directory": ("STRING", {"placeholder": "Image Directory"}),
                "selection_mode": (
                    selection_mode,
                    {"default": "random"},
                ),
            }
        }

    def ImageLoader(self, sub_directory, selection_mode):
        tagger.set_start_time()
        tagger.curr_sub_dir = sub_directory
        directory = os.path.join(folder_paths.get_output_directory(), sub_directory)

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

        chosen_image = self.SELECTION_MODE[selection_mode](image_files)
        chosen_image_path = os.path.join(directory, chosen_image)
        image, mask, prompt_text = get_comfy_image_mask(chosen_image_path)
        tagger.process_file(directory, chosen_image)
        return (image, mask, prompt_text)


class WorkflowImageSaver:
    CATEGORY = "feidorian/workflow-manager"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "ImageSaver"
    type = "output"

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return float("nan")
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "prompt_text": ("STRING",{"default":""}),
                "with_workflow": ("BOOLEAN", {"default": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def ImageSaver(self, images, with_workflow, prompt_text, prompt=None, extra_pnginfo=None):
        path = tagger.curr_dir
        results = list()
        if not path:
            raise Exception("Missing Path. Path must be provided to loader node.")
        filename = tagger.curr_product_filename
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = PngInfo()
            metadata.add_text("prompt_text", prompt_text)
            if with_workflow:
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            file = f"{filename}.png"
            img.save(os.path.join(path, file), pnginfo=metadata, compress_level=4)
            results.append({
                "filename": file,
                "subfolder": tagger.curr_sub_dir,
                "type": self.type
            })
  
        tagger.log_time()
        return {"ui": {"images": results}}
