# Import default settings
from .settings_dist import *

# Import custom settings
try:
    from settings import *
except ImportError:
    pass
