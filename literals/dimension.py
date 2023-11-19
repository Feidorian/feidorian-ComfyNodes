from nodes import MAX_RESOLUTION



class Feidorian_dimensionLiteral:
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("dimension",)
    FUNCTION = "get_int"
    CATEGORY = "feidorian/literals"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"int": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 8})}}

    def get_int(self, int):
        return (int,)
