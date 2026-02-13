# Location: core/__init__.py

from .bin_state import BinState
from .waste_database import WasteDatabase
from .aggregation import add_waste
from .scoring import compute_microbial_activity
from .decay import apply_decay

# This allows your app.py to see these modules as a package