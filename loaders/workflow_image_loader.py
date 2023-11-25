"""
@Author: Feidorian
@Platform: ComfyUI

@Description:
    * Workflow Image Loader Iterates through unprocessed files in a working directory and returns each per call.
    * Each unprocessed file that is selected will be marked with a processed prefix (appended to original filename).
    * The original filename (appended with a Product prefix) will be returned by the function for proper labeling of product files.
    * Each file that either contains a processed or product prefix will be ignored by the selection process.
    * If all files contain both processed and product variants, an error is thrown as the workflow's task is complete.
    * If a file exists as a processed variant without an equivalent product variant:
        * A past error occured preventing the creation of a product variant
        * The file's name should be reverted to the original name (marked as unprocessed)
    * Options
        * is_random: unprocessed files are selected at random
        * is_processed: enables tagging files with prefixes. If false, no tracking/checks occurs, and selection is infinite.


@Status: Incomplete
@FIXME:
    * Processed prefix is immutable
        * All files with processed prefix will be ignored
    * Product prefix has defaults with custom option
        * Product prefix must have defaults and a custom option
@TODO:
    * Testing (Production)
"""

import torch
import random
import os
from PIL import Image, ImageOps
from itertools import repeat
import numpy as np
from datetime import datetime, timedelta
from ..log import log
from ..utils import ellapsed_tracker

