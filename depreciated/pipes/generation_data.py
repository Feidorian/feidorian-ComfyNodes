
import comfy.sd
from nodes import MAX_RESOLUTION
import folder_paths

class Feidorian_GenerationDataPipeEdit:

  CATEGORY = "feidorian/pipes"
  RETURN_TYPES = (
    "STRING",
    "STRING",
    folder_paths.get_filename_list("checkpoints"),
    comfy.samplers.KSampler.SAMPLERS,
    comfy.samplers.KSampler.SCHEDULERS,
    "FLOAT",
    "INT",
    "INT",
    "INT",
    "INT",
    "GDATAPIPE"
    )
  RETURN_NAMES = ("Positive","Negative", "Model", "Sampler", "Scheduler","CFG","Steps","Seed","Width","Height","GDataPipe")
  FUNCTION = "GenerationDataPipeEdit"


  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "GDataPipe": ("GDATAPIPE",)
      },
      "optional":{
        "positive": ("STRING", {"forceInput":True}),
        "negative": ("STRING", {"forceInput":True}),
        "model": (folder_paths.get_filename_list("checkpoints"),{"forceInput":True}),
        "sampler": (comfy.samplers.KSampler.SAMPLERS,{"forceInput":True}),
        "scheduler": (comfy.samplers.KSampler.SCHEDULERS,{"forceInput":True}),
        "cfg": ("FLOAT", { "min": 0.0, "max": 100.0, "forceInput":True}),
        "steps": ("INT", {"min": 1, "max": 10000, "forceInput":True}),
        "seed": ("INT", {"min": 0, "max": 0xffffffffffffffff, "forceInput":True}),
        "width": ("INT", {"min": 1, "max": MAX_RESOLUTION, "step": 8, "forceInput":True}),
        "height": ("INT", {"min": 1, "max": MAX_RESOLUTION, "step": 8, "forceInput":True}),
      }
    }


  def GenerationDataPipeEdit(self, GDataPipe, positive=None, negative=None, model=None,
                             sampler=None, scheduler=None, cfg=None, steps=None, seed=None, width=None, height=None):

    Positive = positive if positive else GDataPipe[0]
    Negative = negative if negative else GDataPipe[1]
    Model = model if model else GDataPipe[2]
    Sampler = sampler if sampler else GDataPipe[3]
    Scheduler = scheduler if scheduler else GDataPipe[4]
    CFG = cfg if cfg else GDataPipe[5]
    Steps = steps if steps else GDataPipe[6]
    Seed = seed if seed else GDataPipe[7]
    Width = width if width else GDataPipe[8]
    Height = height if height else GDataPipe[9]
    GDataPipe = (Positive,Negative, Model, Sampler, Scheduler, CFG, Steps, Seed, Width, Height)
    return (Positive,Negative, Model, Sampler, Scheduler, CFG, Steps, Seed, Width, Height,GDataPipe)


class FeidorianGenerationDataProvider:

  CATEGORY = "feidorian/pipes"
  RETURN_TYPES = (
    "STRING",
    "STRING",
    folder_paths.get_filename_list("checkpoints"),
    comfy.samplers.KSampler.SAMPLERS,
    comfy.samplers.KSampler.SCHEDULERS,
    "FLOAT",
    "INT",
    "INT",
    "INT",
    "INT",
    "GDATAPIPE"
    )
  RETURN_NAMES = ("Positive","Negative", "Model", "Sampler", "Scheduler","CFG","Steps","Seed","Width","Height","GDataPipe")
  FUNCTION = "GenerationDataProvider"

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "positive": ("STRING", {"default": '', "multiline": True, "placeholder":"Positive"}),
        "negative": ("STRING", {"default": '', "multiline": True, "placeholder":"Negative"}),
        "model": (folder_paths.get_filename_list("checkpoints"),),
        "sampler": (comfy.samplers.KSampler.SAMPLERS,),
        "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
        "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
        "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
        "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
        "width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 8}),
        "height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 8}),
      },
      "optional":{
        "GDataPipe":("GDATAPIPE",),
      }
    }



  def GenerationDataProvider(self, positive, negative, model, sampler, scheduler, cfg, steps, seed, width, height, GDataPipe=None):

    Positive = GDataPipe[0] if GDataPipe and GDataPipe[0] else positive
    Negative = GDataPipe[1] if GDataPipe and GDataPipe[1] else negative
    Model = GDataPipe[2] if GDataPipe and GDataPipe[2] else model
    Sampler = GDataPipe[3] if GDataPipe and GDataPipe[3] else sampler
    Scheduler = GDataPipe[4] if GDataPipe and GDataPipe[4] else scheduler
    CFG = GDataPipe[5] if GDataPipe and GDataPipe[5] else cfg
    Steps = GDataPipe[6] if GDataPipe and GDataPipe[6] else steps
    Seed = GDataPipe[7] if GDataPipe and GDataPipe[7] else seed
    Width = GDataPipe[8] if GDataPipe and GDataPipe[8] else width
    Height = GDataPipe[9] if GDataPipe and GDataPipe[9] else height

    new_pipe = (Positive, Negative, Model, Sampler, Scheduler, CFG, Steps, Seed, Width, Height)

    return (
      Positive,
      Negative,
      Model,
      Sampler,
      Scheduler,
      CFG,
      Steps,
      Seed,
      Width,
      Height,
      new_pipe
    )