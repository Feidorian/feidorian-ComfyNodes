import folder_paths
import time
import re
import os
import numpy as np
import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import comfy.sd
from nodes import MAX_RESOLUTION


class Feidorian_ImageSave:
  CATEGORY = "feidorian/output"
  RETURN_TYPES = ()
  OUTPUT_NODE = True
  FUNCTION = "ImageSave"
  output_dir = folder_paths.get_output_directory()
  type = "output"

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "images":("IMAGE",),
        "sub_dir":("STRING",{"default":""}),
        "opt_Filename":("STRING",{"default":""}),
        "prompt_text":("STRING",{"default":""}),
        "with_workflow": ("BOOLEAN",{"default":True}),
      },
      "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
    }

  def ImageSave(self, images, sub_dir, opt_Filename, prompt_text, with_workflow, prompt=None, extra_pnginfo=None):
    path = os.path.join(self.output_dir, sub_dir)
    results = list()
    if not path:
        raise Exception("Missing Path. Path must be provided to loader node.")
    filename = opt_Filename if opt_Filename else time.strftime("%Y%m%d-%H%M%S")
    for image in images:
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        metadata = PngInfo()
        if prompt_text:
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
            "subfolder": sub_dir,
            "type": self.type
        })

    return {"ui": {"images": results}}







