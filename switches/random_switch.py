"""
@Author: Feidorian
Made for ComfyUI
"""

from ..utils import ANY_TYPE
import random


class Feidorian_RandomSwitch:
    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("VALUE",)
    FUNCTION = "RandomSwitch"
    CATEGORY = "feidorian/switches"

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "value1": (ANY_TYPE,),
                "value2": (ANY_TYPE,)
            }
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")


    def RandomSwitch(self, value1: ANY_TYPE, value2: ANY_TYPE) -> ANY_TYPE:
        value = random.choice([value1, value2])
        return (value,)
