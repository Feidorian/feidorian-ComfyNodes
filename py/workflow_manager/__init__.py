from .image_tagger import WorkflowImageLoader, WorkflowImageSaver
from .image_tagger_advanced import WorkflowImageLoaderAdvanced, WorkflowImageSaverAdvanced
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
        {
            "name": "Feidorian_WorkflowImageLoaderAdvanced",
            "function": WorkflowImageLoaderAdvanced,
            "display_name": "FD Workflow Image Loader Advanced",
        },
        {
            "name": "Feidorian_WorkflowImageSaverAdvanced",
            "function": WorkflowImageSaverAdvanced,
            "display_name": "FD Workflow Image Saver Advanced",
        },
    ]
)
