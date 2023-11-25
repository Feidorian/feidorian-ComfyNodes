from ...utils import ANY_TYPE


class Feidorian_AOrB:
    CATEGORY = "feidorian/logic"
    RETURN_NAMES = "C"
    RETURN_TYPES = ANY_TYPE
    FUNCTION = "AOrB"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "A": (ANY_TYPE,),
                "B": (ANY_TYPE,),
                "a_is_true": ("BOOLEAN", {"default": True}),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    def AOrB(self, A, B, a_is_true):
        return (A if a_is_true else B,)
