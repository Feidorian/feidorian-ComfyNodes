from .any_switch import Feidorian_AnySwitch
from .random_switch import Feidorian_RandomSwitch
from ..utils import generate_mappings


mappings = generate_mappings(
    [
        {
            "name": "Feidorian_AnySwitch",
            "function": Feidorian_AnySwitch,
            "display_name": "FD Any Switch",
        },
        {
            "name": "Feidorian_RandomSwitch",
            "function": Feidorian_RandomSwitch,
            "display_name": "FD Random Switch",
        },
   
    ]
)
