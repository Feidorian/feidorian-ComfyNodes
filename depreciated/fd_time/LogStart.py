from ..utils import ANY_TYPE, ellapsed_tracker

class Feidorian_LogStart:

  CATEGORY = "feidorian/time"
  OUTPUT_NODE = True
  RETURN_TYPES = ()
  FUNCTION = "LogStart"


  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required":{
        "node":(ANY_TYPE,)
      }
    }

  def LogStart(self, **argv):
    ellapsed_tracker.log_start()
    return ()