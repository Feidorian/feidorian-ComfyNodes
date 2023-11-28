"""
@Author: Feidorian
Made for ComfyUI
"""

from ...utils import ANY_TYPE


class Feidorian_AnySwitch:
    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("VALUE",)
    FUNCTION = "AnySwitch"
    CATEGORY = "feidorian/switches"

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "value1": (ANY_TYPE,),
                "value2": (ANY_TYPE,),
                "Input": (
                    "INT",
                    {"default": 1, "min": 1, "max": 2, "step": 1},
                ),
            }
        }

    def AnySwitch(self, value1: ANY_TYPE, value2: ANY_TYPE, Input: int) -> ANY_TYPE:
        return (value1 if Input == 1 else value2,)
