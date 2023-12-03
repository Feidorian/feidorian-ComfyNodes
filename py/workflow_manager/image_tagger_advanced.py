"""
# Process Step Categories
1. Fix Errors (processed variants without product variants)
2. Approve products (product variants without processed variants)
3. Select An Image (via selection mode; ex. random, ascending, descending, etc)
4. Process The Selected Image (tagging, transformation, product generation).
"""

import math
import random
import shutil
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


class ImageTagger:
    PRODUCT_TAG = "product_"
    PROCESSED_TAG = "processed_"

    BASE_DIRECTORY = os.path.join(
        folder_paths.get_output_directory(), "WORKFLOW_IMAGES_ADVANCED"
    )
    APPROVED_DIRECTORY = os.path.join(BASE_DIRECTORY, "APPROVED_IMAGES")
    CACHED_DIRECTORY = os.path.join(BASE_DIRECTORY, "CACHED_IMAGEs")
    PROTECTED_DIRECTORY_PATHS = [BASE_DIRECTORY, APPROVED_DIRECTORY, CACHED_DIRECTORY]

    status_params = {
        "start_time": None,
        "end_time": None,
        "processed_file_count": 0,
        "unprocessed_file_count": 0,
    }

    tracking_params = {"file_name": None, "file_dir": None}

    def __init__(self):
        self.__create_dir(self.BASE_DIRECTORY)
        self.__create_dir(self.APPROVED_DIRECTORY)
        self.__create_dir(self.CACHED_DIRECTORY)

    def __create_dir(self, dir: str) -> None:
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                log.debug(f"Directory '{dir}' created successfully.")
            else:
                log.debug(f"Directory '{dir}' already exists.")
        except OSError as e:
            raise Exception(f"Error creating Directory '{dir}': {e}")

    def __is_valid_image(file_path: str) -> bool:
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except:
            return False

    def start_timer(self):
        self.status_params["start_time"] = datetime.now()

    def end_timer(self):
        self.status_params["end_time"] = datetime.now()

    def fix_errors_and_approve_products(self):
        self.status_params["processed_file_count"] = 0
        non_protected_directory_paths = []
        for directory in os.listdir(self.BASE_DIRECTORY):
            dir_path = os.path.join(self.BASE_DIRECTORY, directory)
            if not os.path.isdir(dir_path):
                continue
            if dir_path in self.PROTECTED_DIRECTORY_PATHS:
                continue
            non_protected_directory_paths.append(dir_path)

        # Iterate each non-protected directory
        for dir_path in non_protected_directory_paths:
            # Delete all non-image files from directory.
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if not self.__is_valid_image(file_path):
                    os.remove(file_path)

            processed_files = [
                file for file in os.listdir(dir_path) if self.PROCESSED_TAG in file
            ]
            product_files = [
                file for file in os.listdir(dir_path) if self.PRODUCT_TAG in file
            ]
            tagged_files = processed_files + product_files
            untagged_files = list(set(os.listdir(dir_path)) - set(tagged_files))

            # Raise a corrupted directory exception if it is the case that:
            # An untagged image file exists in the directory.
            if untagged_files:
                raise Exception(
                    f"Corrupted directory '{dir_path}': presence of untagged files."
                )
            # More than 1 image file of the same tag exists in the directory.
            elif len(processed_files) > 1 or len(product_files) > 1:
                raise Exception(
                    f"Corrupted directory '{dir_path}': Presence of more than 1 file of the same tag."
                )
            # More than two image files exist in the directory.
            elif len(tagged_files + untagged_files) > 2:
                raise Exception(
                    f"Corrupted directory '{dir_path}': More than 2 image files in directory."
                )

            # If a processed file exists without a product file:
            if len(processed_files) == 1 and not product_files:
                # Untag the file and move it to the base directory
                untagged_file = processed_files[0].replace(self.PROCESSED_TAG, "")
                old_path = os.path.join(dir_path, processed_files[0])
                new_path = os.path.join(self.BASE_DIRECTORY, untagged_file)
                os.rename(old_path, new_path)
                # Delete the non-protected directory
                shutil.rmtree(dir_path)
            else:
                self.status_params["processed_file_count"] += 1

            # If a product file exists without a processed file:
            if len(product_files) == 1 and not processed_files:
                # Untag the file and move it to a protected directory
                untagged_file = product_files[0].replace(self.PRODUCT_TAG, "")
                old_path = os.path.join(dir_path, product_files[0])
                new_path = os.path.join(self.APPROVED_DIRECTORY, untagged_file)
                os.rename(old_path, new_path)
                # Delete the non-protected directory
                shutil.rmtree(dir_path)

    def select_and_prepare_image_file(self, select_func):
        valid_image_files = []
        # Iterate the base directory
        for child in os.listdir(self.BASE_DIRECTORY):
            child_path = os.path.join(self.BASE_DIRECTORY, child)
            # Ignore all sub-directories and non image files
            if os.path.isdir(child_path):
                continue
            if not self.__is_valid_image(child_path):
                continue
            # Curate all image files into a list
            valid_image_files.append(child)

        # Check if there is at least one valid image file
        if not valid_image_files:
            raise Exception(
                f"No valid image files found in the base directory {self.BASE_DIRECTORY}."
            )

        self.status_params["unprocessed_file_count"] = len(valid_image_files)

        # Apply a selection function to the list to derive a selected image file
        selected_image = select_func(valid_image_files)
        selected_image_path = os.path.join(self.BASE_DIRECTORY, selected_image)
        # Create a sub-directory, naming it with the file's name (without extension)
        base_file_name, base_file_ext = os.path.splitext(selected_image)
        sub_directory = os.path.join(self.BASE_DIRECTORY, base_file_name)
        # Raise Exception if subdirectory exists
        if os.path.exists(sub_directory):
            raise Exception(f"Directory '{sub_directory}' already exists.")
        processed_file_variant = self.PROCESSED_TAG + base_file_name + base_file_ext
        product_file_variant = self.PRODUCT_TAG + base_file_name + base_file_ext
        # rename selected file to processed file name variant
        os.rename(
            selected_image_path,
            os.path.join(self.BASE_DIRECTORY, processed_file_variant),
        )
        # get path of renamed image
        selected_image_path = os.path.join(self.BASE_DIRECTORY, processed_file_variant)
        # move file to subdirectory and get new path
        selected_image_path = shutil.move(selected_image_path, sub_directory)
        self.tracking_params["file_name"] = product_file_variant
        self.tracking_params["file_dir"] = sub_directory
        return selected_image_path

    @staticmethod
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

    @staticmethod
    def random_picker(images: list[str]) -> str:
        return random.choice(images)

    @staticmethod
    def linear_picker(images: list[str]) -> str:
        return images[0]

    def log_status(self):
        # if not self.start_time:
        #     return
        # self.processed_file_count += 1
        # self.unprocessed_file_count -= 1
        # current_time = datetime.now()
        # approx_time = math.ceil((current_time - self.start_time).total_seconds())
        # remaining_time = self.unprocessed_file_count * approx_time
        # log.info("**** Workflow Image Manager Status ****")
        # log.info(f"Number of Tasks Completed: {self.processed_file_count}")
        # log.info(f"Number of Tasks Left: {self.unprocessed_file_count}")
        # log.info(f"Number of Detected Errors: {self.error_file_count}")
        # log.info(f"Previous Completion Time: {timedelta(seconds=approx_time)}")
        # log.info(f"Remaining Time (Estimate): {timedelta(seconds=remaining_time)}")
        # self.__reset__()
        pass


tagger = ImageTagger()


class WorkflowImageLoaderAdvanced:
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
                "selection_mode": (
                    selection_mode,
                    {"default": "random"},
                ),
            }
        }

    def ImageLoader(self, selection_mode):
        tagger.fix_errors_and_approve_products()
        selected_file_path = tagger.select_and_prepare_image_file(
            self.SELECTION_MODE[selection_mode]
        )
        return tagger.get_comfy_image_mask(selected_file_path)


class WorkflowImageSaverAdvanced:
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
                "prompt_text": ("STRING", {"default": ""}),
                "with_workflow": ("BOOLEAN", {"default": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def ImageSaver(
        self, images, with_workflow, prompt_text, prompt=None, extra_pnginfo=None
    ):
        pass
        # path = tagger.curr_dir
        # results = list()
        # if not path:
        #     raise Exception("Missing Path. Path must be provided to loader node.")
        # filename = tagger.curr_product_filename
        # for image in images:
        #     i = 255.0 * image.cpu().numpy()
        #     img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        #     metadata = PngInfo()
        #     metadata.add_text("prompt_text", prompt_text)
        #     if with_workflow:
        #         if prompt is not None:
        #             metadata.add_text("prompt", json.dumps(prompt))
        #         if extra_pnginfo is not None:
        #             for x in extra_pnginfo:
        #                 metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        #     file = f"{filename}.png"
        #     img.save(os.path.join(path, file), pnginfo=metadata, compress_level=4)
        #     results.append(
        #         {"filename": file, "subfolder": tagger.curr_sub_dir, "type": self.type}
        #     )

        # tagger.log_time()
        # return {"ui": {"images": results}}
