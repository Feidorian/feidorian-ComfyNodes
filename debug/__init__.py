"""
@Author: Feidorian
@Description: Central Node Accumulator for debug nodes

Made for ComfyUI
"""


from .null_output import Feidorian_NullOutput
from ..utils import generate_mappings



mappings = generate_mappings([
  {"name":"Feidorian_NullOutput", "function":Feidorian_NullOutput, "display_name":"FD Null Output"}
])
