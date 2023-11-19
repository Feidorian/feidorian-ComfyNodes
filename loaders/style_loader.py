import folder_paths
import csv
from ..log import log
from pathlib import Path


def load_CSV(cls):
    if not cls.options:
        input_dir = Path(folder_paths.base_path) / "styles"
        if not input_dir.exists():
            log.warn("Styles directory does not exist")

        if not (files := [f for f in input_dir.iterdir() if f.suffix == ".csv"]):
            log.warn(
                    "No styles found in the styles folder, place at least one csv file in the\
                    styles folder at the root of ComfyUI (for instance ComfyUI/styles/mystyle.csv)"
                )

        for file in files:
            with open(file, "r", encoding="utf8") as f:
                parsed = csv.reader(f)
                for row in parsed:
                    if row[0] == "name":
                        cls.options["None"] = ("","")
                        continue
                    log.debug(f"Adding style {row[0]}")
                    cls.options[row[0]] = (row[1], row[2])

    else:
        log.debug(f"Using cached styles (count: {len(cls.options)})")


class Feidorian_StylesLoader:
    """Load csv files and populate a dropdown from the rows (à la A111)"""

    options = {}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "loadStyle"
    CATEGORY = "feidorian/loaders"

    @classmethod
    def INPUT_TYPES(cls):
        load_CSV(cls)
        return {
            "required": {
                "style_name": (list(cls.options.keys()),),
                "optional_positive": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    def loadStyle(self, style_name, optional_positive):
        positive = f"{self.options[style_name][0]}, {optional_positive}"
        negative = self.options[style_name][1]
        return (positive, negative)





class Feidorian_TextEncodedStylesLoader:
    """Load csv files and populate a dropdown from the rows (à la A111)"""

    options = {}
    RETURN_TYPES = ("CONDITIONING","CONDITIONING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "loadTextEncodedStyle"
    CATEGORY = "feidorian/loaders"

    @classmethod
    def INPUT_TYPES(cls):
        load_CSV(cls)
        return {
            "required": {
                "style_name": (list(cls.options.keys()),),
                "positive_text": ("STRING", {"multiline": True, "default": ""}),
                "clip": ("CLIP", )
            }
        }

    def loadTextEncodedStyle(self, style_name, positive_text,clip):
        positive_text = f"{self.options[style_name][0]}, {positive_text}"
        negative_text = self.options[style_name][1]

        positive_tokens = clip.tokenize(positive_text)
        positive_cond, positive_pooled = clip.encode_from_tokens(positive_tokens, return_pooled=True)
        positive = [[positive_cond, {"pooled_output": positive_pooled}]]

        negative_tokens = clip.tokenize(negative_text)
        negative_cond, negative_pooled = clip.encode_from_tokens(negative_tokens, return_pooled=True)
        negative = [[negative_cond, {"pooled_output": negative_pooled}]]
        return (positive, negative)
