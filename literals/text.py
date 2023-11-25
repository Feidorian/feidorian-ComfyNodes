
class Feidorian_TextLiteral:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "get_text"
    CATEGORY = "feidorian/literal"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"string": ("STRING", {"default": "", "multiline": False})}}

    def get_text(self, string):
        return (string,)

class Feidorian_TextBoxLiteral:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "get_text_box"
    CATEGORY = "feidorian/literal"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"string": ("STRING", {"default": "", "multiline": True})}}

    def get_text_box(self, string):
        return (string,)

class Feidorian_TextConcat:
    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("A_plus_b","B_plus_A")
    FUNCTION = "get_concated_text"
    CATEGORY = "feidorian/concat"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required":{
                "text_A": ("STRING", {"default": "", "multiline": True}),
                "text_B": ("STRING", {"default":"", "multiline": True}),
                "delimeter":("STRING",{"default":", "})
             }}

    def get_concated_text(self, text_A, text_B, delimeter):
        if text_A and not text_B: return (text_A, text_A)
        elif text_B and not text_A: return (text_B, text_B)
        output_AB = f"{text_A}{delimeter}{text_B}"
        output_BA = f"{text_B}{delimeter}{text_A}"

        return (output_AB, output_BA)
