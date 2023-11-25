from .style_loader import Feidorian_StylesLoader, Feidorian_TextEncodedStylesLoader
# from .workflow_image_loader import Feidorian_WorkflowImageLoader
from ...utils import generate_mappings



mappings = generate_mappings([
  {"name":"Feidorian_StyleLoader", "function":Feidorian_StylesLoader, "display_name":"FD Style Loader"},
  # {"name":"Feidorian_WorkflowImageLoader", "function":Feidorian_WorkflowImageLoader, "display_name":"FD WorkflowImageLoader"},
  {"name":"Feidorian_TextEncodedStyleLoader", "function":Feidorian_TextEncodedStylesLoader, "display_name":"FD TextEncoded Style"}
])