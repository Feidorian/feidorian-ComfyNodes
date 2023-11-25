"""
@Author: Feidorian
@Description: Central Node Accumulator for all active nodes

Made for ComfyUI
"""
import os, shutil
import folder_paths

from .py import output
from .py import switches
from .py import loaders
from .py import debug
from .py import logic
from .py import literals
from .py import workflow_manager

NODES = [output, switches, loaders, debug, logic, literals, workflow_manager]


################## DO NOT EDIT PAST (BELOW) THIS LINE #####################################################

NODE_CLASS_MAPPINGS = []
NODE_DISPLAY_NAME_MAPPINGS = []
for node in NODES:
    NODE_CLASS_MAPPINGS += node.mappings["NODE_CLASS_MAPPINGS"]
    NODE_DISPLAY_NAME_MAPPINGS += node.mappings["NODE_DISPLAY_NAME_MAPPINGS"]

NODE_CLASS_MAPPINGS = dict(NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS = dict(NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

print("\033[34mFeidorian Custom Nodes: \033[92mLoaded\033[0m")


module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(
    application_root_directory, "web", "extensions", "Feidorian_Extensions"
)

shutil.copytree(
    module_js_directory, application_web_extensions_directory, dirs_exist_ok=True
)
print("\033[34mFeidorian Custom Extenstions: \033[92mLoaded\033[0m")
