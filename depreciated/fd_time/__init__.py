from .LogEnd import Feidorian_LogEnd
from .LogStart import Feidorian_LogStart
from ..utils import generate_mappings


mappings = generate_mappings([
  {"name":"Feidorian_LogStart", "function":Feidorian_LogStart, "display_name":"FD Log Start"},
  {"name":"Feidorian_LogEnd", "function":Feidorian_LogEnd, "display_name":"FD Log End"}
])


