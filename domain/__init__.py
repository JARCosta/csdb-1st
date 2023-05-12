# Define package-level attributes and constants
__version__ = '1.0'
MAX_RETRIES = 5

# Import modules and sub-packages
from .root import *
from .inventory import *
from .prices import *
from .database import *

# Execute code on package import
print('Package domain initialized')