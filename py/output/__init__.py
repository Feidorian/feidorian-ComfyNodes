from .image_save import Feidorian_ImageSave
from ...utils import generate_mappings

mappings  = generate_mappings(
  [
    {"name":"Feidorian_ImageSave", "function": Feidorian_ImageSave, "display_name":"FD Image Save"}
  ])
