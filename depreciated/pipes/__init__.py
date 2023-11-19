from .generation_data import Feidorian_GenerationDataPipeEdit, FeidorianGenerationDataProvider

from ..utils import generate_mappings



mappings = generate_mappings([
  {"name":"Feidorian_GenerationDataPipeEdit", "function":Feidorian_GenerationDataPipeEdit, "display_name":"FD Gen Data PipeEdit"},
  {"name":"Feidorian_GenerationDataProvider", "function":FeidorianGenerationDataProvider, "display_name":"FD Gen Data Provider"}
])



