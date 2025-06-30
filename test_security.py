#!/usr/bin/env python3
"""
Security tests for the code execution functionality.
Tests that malicious code is blocked while legitimate code works.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import execute_code

def test_safe_code():
    """Test that safe code executes correctly"""
    safe_codes = [
        'print("Hello World")',
        'x = 5\nprint(x * 2)',
        'for i in range(3):\n    print(i)',
        'def greet(name):\n    return f"Hello {name}"\nprint(greet("World"))',
        'import math\nprint(math.sqrt(16))'
    ]
    
    for code in safe_codes:
        try:
            result = execute_code(code)
            print(f"✓ Safe code executed: {repr(code[:30])}... -> {repr(result[:50])}")
        except Exception as e:
            print(f"✗ Safe code failed: {repr(code[:30])}... -> {e}")

def test_malicious_code():
    """Test that malicious code is blocked"""
    malicious_codes = [
        # File system access
        'import os\nos.system("rm -rf /")',
        'open("/etc/passwd", "r").read()',
        
        # Network access
        'import urllib.request\nurllib.request.urlopen("http://evil.com")',
        
        # Process manipulation
        'import subprocess\nsubprocess.call(["ls", "/"])',
        
        # System information
        'import os\nprint(os.environ)',
        
        # Module manipulation
        'import sys\nsys.exit(1)',
        
        # Dangerous built-ins
        '__import__("os").system("whoami")',
        'eval("__import__(\'os\').system(\'whoami\')")',
        'exec("import os; os.system(\'whoami\')")',
    ]
    
    for code in malicious_codes:
        try:
            result = execute_code(code)
            print(f"✗ Malicious code executed (SECURITY ISSUE): {repr(code[:50])}... -> {repr(result[:50])}")
        except Exception as e:
            print(f"✓ Malicious code blocked: {repr(code[:50])}... -> {type(e).__name__}: {str(e)[:50]}")

if __name__ == "__main__":
    print("=== Testing Current Implementation ===")
    print("\n--- Testing Safe Code ---")
    test_safe_code()
    print("\n--- Testing Malicious Code ---")
    test_malicious_code()