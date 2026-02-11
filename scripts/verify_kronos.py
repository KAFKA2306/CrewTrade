import sys
try:
    from model import Kronos
    print("SUCCESS: Successfully imported Kronos from model module.")
except ImportError as e:
    print(f"FAILURE: Could not import Kronos. {e}")
    sys.exit(1)
except Exception as e:
    print(f"FAILURE: Unexpected error. {e}")
    sys.exit(1)
