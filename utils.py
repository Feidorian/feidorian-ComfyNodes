"""
@Author: Feidorian
"""

from contextlib import contextmanager
import io
import sys
from datetime import datetime, timedelta
import math

@contextmanager
def suppress_output():
    """
    Suppress standard output in code block

    Usage:
        with suppress_output():
            code
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        yield
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


ANY_TYPE = AnyType("*")


def generate_mappings(mappings):
    NODE_CLASS_MAPPINGS = [(item["name"], item["function"]) for item in mappings]
    NODE_DISPLAY_NAME_MAPPINGS = [(item["name"], item["display_name"]) for item in mappings]
    return {"NODE_CLASS_MAPPINGS":NODE_CLASS_MAPPINGS, "NODE_DISPLAY_NAME_MAPPINGS":NODE_DISPLAY_NAME_MAPPINGS}



class EllapsedTracker:

    def __init__(self):
        self.approx_time = None
        self.current_start_time = None

    def log_start(self):
        self.current_start_time = datetime.now()

    def log_end(self):
        if self.current_start_time:
            time = datetime.now()
            approx_time = (time - self.current_start_time).total_seconds()
            # if self.approx_time: self.approx_time = math.ceil((self.approx_time + approx_time)/2)
        # else:
            self.approx_time = math.ceil(approx_time)

    def get_ellapsed(self):
        return self.approx_time


ellapsed_tracker = EllapsedTracker()
