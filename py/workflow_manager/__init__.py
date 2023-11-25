from .image_tagger import WorkflowImageLoader, WorkflowImageSaver
from ...utils import generate_mappings

mappings = generate_mappings(
    [
        {
            "name": "Feidorian_WorkflowImageLoader",
            "function": WorkflowImageLoader,
            "display_name": "FD Workflow Image Loader",
        },
        {
            "name": "Feidorian_WorkflowImageSaver",
            "function": WorkflowImageSaver,
            "display_name": "FD Workflow Image Saver",
        },
    ]
)
