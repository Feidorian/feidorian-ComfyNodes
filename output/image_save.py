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
        "Images":("IMAGE",),
        "Path":("STRING",{"default":""}),
        "Opt_Filename":("STRING",{"default":""}),
        "Ext":("STRING",{"default":"png"}),
        "with_workflow": ("BOOLEAN",{"default":True}),
        "date_is_required":("BOOLEAN",{"default":False})
      },
      "optional":{
        "GDataPipe":("GDATAPIPE",)
        },
        "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
    }

  #TODO: add other metadata info equiv to imagesave with metada and delete the imagesave w metadata extension
  def ImageSave(self, Images, Path, Opt_Filename, Ext, with_workflow, date_is_required, GDataPipe=None, prompt=None, extra_pnginfo=None):

    if not Path: Path = self.output_dir
    if not os.path.isdir(Path): raise Exception(f"path: {Path} does not exist")

    is_unique = Opt_Filename and date_is_required
    date_filename = time.strftime("%Y%m%d-%H%M%S")
    if not Opt_Filename: Opt_Filename = date_filename
    else: Opt_Filename = re.sub(r"\s+", '-', Opt_Filename)

    if is_unique: Opt_Filename = f"{Opt_Filename}_{date_filename}"

    # if not Ext: Ext = "png"
    # elif Ext.lower() != "png": raise Exception("Only png extension formats allowed")
    # else: Ext = Ext.lower()
    Ext = "png"

    img_count = 0;
    results = list()
    for img in Images:
      img_count += 1
      save_filename = Opt_Filename
      if Images.size()[0] > 1: save_filename = f"{Opt_Filename}_{img_count:05d}"
      final_filename = f"{save_filename}.{Ext}"

      i = 255. * img.cpu().numpy()
      img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
      metadata = PngInfo() if GDataPipe or with_workflow else None

      if with_workflow:
        if prompt is not None:
          metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
          for x in extra_pnginfo:
            metadata.add_text(x, json.dumps(extra_pnginfo[x]))
      if GDataPipe:
        metadata.add_text("Positive", str(GDataPipe[0]))
        metadata.add_text("Negative", str(GDataPipe[1]))
        metadata.add_text("Model", str(GDataPipe[2]))
        metadata.add_text("Sampler", str(GDataPipe[3]))
        metadata.add_text("Scheduler", str(GDataPipe[4]))
        metadata.add_text("CFG", str(GDataPipe[5]))
        metadata.add_text("Steps", str(GDataPipe[6]))
        metadata.add_text("Seed", str(GDataPipe[7]))
        metadata.add_text("Width", str(GDataPipe[8]))
        metadata.add_text("Height", str(GDataPipe[9]))
      # print(GDataPipe, "was here")

      img.save(os.path.join(Path, final_filename), pnginfo=metadata, compress_level=4)
      results.append({ "filename": final_filename,"subfolder":"", "type": self.type})


    return { "ui": { "images": results } }









## Sampler
## Model
## CFGScale
## Steps
## Seed
## ClipSkip
## Positive
## Negative