"""conftest.py — add parent dir to sys.path so tests can import lane_a_context_engine."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
