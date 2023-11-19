"""
@Author: Feidorian
@Platform: ComfyUI

@Description:
    * Workflow Image Loader Iterates through unprocessed files in a working directory and returns each per call.
    * Each unprocessed file that is selected will be marked with a processed prefix (appended to original filename).
    * The original filename (appended with a Product prefix) will be returned by the function for proper labeling of product files.
    * Each file that either contains a processed or product prefix will be ignored by the selection process.
    * If all files contain both processed and product variants, an error is thrown as the workflow's task is complete.
    * If a file exists as a processed variant without an equivalent product variant:
        * A past error occured preventing the creation of a product variant
        * The file's name should be reverted to the original name (marked as unprocessed)
    * Options
        * is_random: unprocessed files are selected at random
        * is_processed: enables tagging files with prefixes. If false, no tracking/checks occurs, and selection is infinite.


@Status: Incomplete
@FIXME:
    * Processed prefix is immutable
        * All files with processed prefix will be ignored
    * Product prefix has defaults with custom option
        * Product prefix must have defaults and a custom option
@TODO:
    * Testing (Production)
"""

import torch
import random
import os
from PIL import Image, ImageOps
from itertools import repeat
import numpy as np
from datetime import datetime, timedelta
from ..log import log
from ..utils import ellapsed_tracker

class Feidorian_WorkflowImageLoader:
    processed_key = "processed"
    upscaled_key = "upscaled"
    upscale_prefixes = ["1x","2x","4x"]

    FUNCTION = "WorkflowImageLoader"
    CATEGORY = "feidorian/loaders"

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "image",
        "mask",
        "path",
        "filename",
        "file_ext",
        "upscale_prefix",
        "upscale_filename",
    )

    def __init__(self):
        self.prev_datetime = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": "", "multiline": False}),
                "upscale_prefix": (
                    cls.upscale_prefixes,
                    {"default": "2x"},
                ),
                "is_random": ("BOOLEAN", {"default": False}),
                "mark_as_processed": ("BOOLEAN", {"default": True}),
            }
        }

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return float("nan")

    def WorkflowImageLoader(
        self, directory, upscale_prefix, is_random, mark_as_processed
    ):

        if not os.path.exists(directory):
            print(f"path: {directory} does not exist")
            return (None,)
        #** use for checking custom prefixes
        # if len(upscale_prefix.split()) > 1:
        #     print(f"No whitespace allowed in upscale_prefix: {upscale_prefix}")
        #     return (None,)


        unprocessedCt, processedCt, errorCt = self.fix_processing_failures(directory, upscale_prefix)
        image_files = []

        upscaled_tag = f"{self.upscaled_key}_{upscale_prefix}"
        for curr_filename in os.listdir(directory):
            if not curr_filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            # Check if the file contains exclusionary tags
            if self.processed_key in curr_filename or upscaled_tag in curr_filename:
                continue

            try:
                # Try to open and verify the image
                file_path = os.path.join(directory, curr_filename)
                img = Image.open(file_path)
                img.verify()
                image_files.append(curr_filename)
            except Exception:
                # Invalid image, remove it and continue
                os.remove(file_path)

        current_time = datetime.now()
        ellapsed_time = ellapsed_tracker.get_ellapsed()
        hours, minutes, seconds, approx_time = (0,0,0,"N/A")
        dir_files_length = len(image_files)
        if ellapsed_time and dir_files_length:
            seconds = ellapsed_time * dir_files_length
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            approx_time = (current_time + timedelta(seconds=ellapsed_time)*dir_files_length).strftime("%I:%M:%S%p, %m/%d/%Y")

        log.info("**** WorkflowImageLoader Status ****")
        log.info(f"Number of Tasks Completed: {processedCt}")
        log.info(f"Number of Tasks Left: {unprocessedCt}")
        log.info(f"Number of Prior Error fixes: {errorCt}")
        log.info(f"Estimated Time Left: {hours:02d}:{minutes:02d}:{seconds:02d}")
        log.info(f"Estimated Completion Time: {approx_time}")

        if not len(image_files):
            print(f"Path: {directory} is empty or fully processed.")
            return (None,)

        # randomly select an image if is random is set to true
        random_image = random.choice(image_files) if is_random else image_files[0]
        # path of the image
        image_path = os.path.join(directory, random_image)
        # path of the image with processed key
        processed_image_path = os.path.join(directory, f"{self.processed_key}_{random_image}")
        # image filename and extension
        filename, file_ext = [(t[0], t[1].strip(".")) for t in [os.path.splitext(random_image)]][0]
        # image file name
        upscale_filename = f"{upscaled_tag}_{filename}"

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

        if mark_as_processed:
            os.rename(image_path, processed_image_path)
        return (
            image,
            mask,
            directory,
            filename,
            file_ext,
            upscale_prefix,
            upscale_filename,
        )


    def fix_processing_failures(self, path, upscale_prefix):
        errorCount = 0
        processed_tag = f"{self.processed_key}_"
        upscaled_tag = f"{self.upscaled_key}_{upscale_prefix}_"
        image_files = [file for file in os.listdir(path) if file.lower().endswith((".jpg", ".jpeg", ".png"))]
        processed_files = [file for file in image_files if processed_tag in file and not upscaled_tag in file]
        upscaled_files = [file for file in image_files if not processed_tag in file and upscaled_tag in file]
        unprocessed_files = [file for file in image_files if not processed_tag in file and not upscaled_tag in file]
        for processed_file in processed_files:
            found = False
            for upscaled_file in upscaled_files:
                if processed_file.replace(processed_tag,"") == upscaled_file.replace(upscaled_tag,""):
                    found = True
                    break
            if not found:
                old_path = os.path.join(path, processed_file)
                new_path = os.path.join(path, processed_file.replace(processed_tag,""))
                os.rename(old_path, new_path)
                errorCount+=1
        processed_count = len(processed_files) - errorCount
        unprocessed_count = len(unprocessed_files) + errorCount
        return (unprocessed_count, processed_count, errorCount)


