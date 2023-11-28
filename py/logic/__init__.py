from ...utils import generate_mappings
from .a_or_b import Feidorian_AOrB
from .first_non_null import Feidorian_FirstNonNull
from .vae_encode_if_any import Feidorian_VAEEncodeIfAny


mappings = generate_mappings(
    [
        {
            "name": "Feidorian_AOrB",
            "function": Feidorian_AOrB,
            "display_name": "FD A OR B",
        },
        {
            "name": "Feidorian_FirstNonNull",
            "function": Feidorian_FirstNonNull,
            "display_name": "FD First Non Null",
        },
        {
            "name": "Feidorian_VaeEncodeIfAny",
            "function": Feidorian_VAEEncodeIfAny,
            "display_name": "FD Vae Encode If Any",
        },
    ]
)
