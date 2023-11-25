from ..utils import generate_mappings
from .text import Feidorian_TextLiteral, Feidorian_TextBoxLiteral, Feidorian_TextConcat


mappings = generate_mappings([
  {"name":"Feidorian_TextLiteral", "function":Feidorian_TextLiteral, "display_name":"FD Text Literal"},
  {"name":"Feidorian_TextBoxLiteral", "function":Feidorian_TextBoxLiteral, "display_name": "FD TextBox Literal"},
  {"name": "Feidorian_TextConcat", "function":Feidorian_TextConcat, "display_name":"FD Text Concat"}
])