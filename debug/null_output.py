"""
@Author: Feidorian
Made for ComfyUI
"""

from ..utils import ANY_TYPE

class Feidorian_NullOutput:

  RETURN_TYPES = (ANY_TYPE,)
  RETURN_NAMES = ('NULL',)
  CATEGORY = "feidorian/debug"
  FUNCTION = "NullOutput"

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "no_effect":("STRING",{"default":"","placeholder":"no-effect"})
      }
    }

  def NullOutput(self, no_effect):
    return (None,)