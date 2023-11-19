"""
@Author: Feidorian
Made for ComfyUI
"""

from ..utils import ANY_TYPE


class Feidorian_FirstNonNull:
    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("VALUE",)
    FUNCTION = "FirstNonNull"
    CATEGORY = "feidorian/logic"

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {},
            "optional":{
                "value1": (ANY_TYPE,),
                "value2": (ANY_TYPE,),
            }
        }

    def FirstNonNull(self, value1=None, value2=None) -> ANY_TYPE:
        print(value1, value2)
        if value1 is None and value2 is None:
            raise Exception("Atleast One Value Input Expected")
        VALUE = value1 if value1 is not None else value2
        return (VALUE,)


