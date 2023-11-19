from ..utils import ANY_TYPE, ellapsed_tracker

class Feidorian_LogEnd:

  CATEGORY = "feidorian/time"
  OUTPUT_NODE = True
  RETURN_TYPES = ()
  FUNCTION = "LogEnd"


  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "node":(ANY_TYPE,)
      }
    }

  def LogEnd(self, **argv):
    ellapsed_tracker.log_end()
    return ()