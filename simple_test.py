#!/usr/bin/env python3
"""
Simple test for direct function call
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import execute_code

# Test basic functionality
print("Testing execute_code directly:")
result = execute_code('x = 5\nprint(x)')
print(f"Result: '{result}'")

result2 = execute_code('print("Hello")')
print(f"Result2: '{result2}'")