from ..utils import ANY_TYPE


class Feidorian_Conditional:
    """Load csv files and populate a dropdown from the rows (à la A111)"""
    def __init__(self):
      self.initCount = 0

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "loadStyle"
    CATEGORY = "feidorian/loaders"

    @classmethod
    def INPUT_TYPES(cls):
      return {
        "required":{
          "initial_expr":(ANY_TYPE,),
          "initial_count":("INT",{"default":0}),
          "max_count":("INT",{"default":5})
        },
        "optional":{
          "loopback_expr":(ANY_TYPE,),
          "loopbackCount"
        }
      }

    def loadStyle(self, style_name, optional_positive):
        positive = f"{self.options[style_name][0]}, {optional_positive}"
        negative = self.options[style_name][1]
        return (positive, negative)
