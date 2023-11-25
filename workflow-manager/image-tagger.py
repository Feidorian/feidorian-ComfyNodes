import random
import torch
import random
import os
from PIL import Image, ImageOps
from itertools import repeat
import numpy as np
from datetime import datetime, timedelta
from ..log import log
from ..utils import is_valid_image, get_comfy_image_mask



def linear_picker(images):
  return images[0]

def random_picker(images: list):
  return random.choice(images)


class ImageTagger:
  PRODUCT_TAG = "product"
  PROCESSED_TAG = "processed"

  curr_orig_filename = None
  curr_processed_filename = None
  curr_product_filename = None
  pass

tagger = ImageTagger()

class WorkflowImageLoader:
  SELECTION_MODE = {
    "linear": linear_picker,
    "random": random_picker
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
    return {
      "required":{
        "directory": ("STRING", {"placeholder":"Image Directory"}),
        "selection_mode": (cls.SELECTION_MODE.keys(), )
      }
    }


  def ImageLoader(self, directory, selection_mode):
    if not os.path.exists(directory):
      raise Exception(f"Directory {directory} does not Exist.")

    image_files = []
    for curr_file in os.listdir(directory):
      if tagger.PROCESSED_TAG in curr_file \
        or tagger.PRODUCT_TAG in curr_file: continue

      curr_path = os.path.join(directory, curr_file)
      if not is_valid_image(curr_path): continue

      image_files.append(curr_file)

    if len(image_files) == 0:
      raise Exception("No Unprocessed File Found!")

    chosen_image = self.SELECTION_MODE(selection_mode)(image_files)
    chosen_image_path = os.path.join(directory, chosen_image)

    return get_comfy_image_mask(chosen_image_path)







  class WorkflowImageSaver:
    pass

