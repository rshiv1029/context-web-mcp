import sys
import os

# Add the parent directory to Python path so pytest can find our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))