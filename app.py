from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
import io
import signal
import ast
import operator

app = Flask(__name__)
socketio = SocketIO(app)


# A function to execute Python code safely in a restricted environment
def execute_code(code):
    try:
        # Basic input validation
        if not code or not isinstance(code, str):
            return "Error: Invalid input"
        
        if len(code) > 10000:  # Limit code length
            return "Error: Code too long (max 10000 characters)"
        
        # Check for dangerous keywords and patterns
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess', 'import socket', 
            'import urllib', 'import requests', 'import shutil', 'import glob',
            'import tempfile', 'import pickle', 'import marshal', 'import ctypes',
            '__import__', 'eval(', 'exec(', 'compile(', 'open(',
            'file(', 'input(', 'raw_input(', 'exit(', 'quit(',
            'reload(', 'vars(', 'locals(', 'globals(', 'dir(',
            'getattr(', 'setattr(', 'delattr(', 'hasattr(',
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return f"Error: Unsafe operation detected: {pattern}"
        
        # Parse the code to check for unsafe AST nodes
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    return "Error: Import statements are not allowed"
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile', 'open', '__import__']:
                        return f"Error: Function '{node.func.id}' is not allowed"
        except SyntaxError as e:
            return f"Syntax Error: {str(e)}"
        
        # Create output capture
        output_lines = []
        
        def safe_print(*args, sep=' ', end='\n', **kwargs):
            line = sep.join(str(arg) for arg in args)
            output_lines.append(line + end)
        
        # Create a minimal safe execution environment 
        safe_builtins = {
            # Safe print function
            'print': safe_print,
            
            # Basic safe built-ins
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'sorted': sorted,
            'reversed': reversed,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
            'pow': pow,
            'divmod': divmod,
            'type': type,
            'isinstance': isinstance,
            'chr': chr,
            'ord': ord,
            'hex': hex,
            'oct': oct,
            'bin': bin,
            'format': format,
            'repr': repr,
            'ascii': ascii,
            'any': any,
            'all': all,
            'filter': filter,
            'map': map,
            
            # Safe math operations
            'add': operator.add,
            'sub': operator.sub,
            'mul': operator.mul,
            'truediv': operator.truediv,
            'floordiv': operator.floordiv,
            'mod': operator.mod,
        }
        
        # Create restricted environment
        safe_environment = {
            '__builtins__': safe_builtins,
            '__name__': '__main__',
        }
        
        # Set up execution timeout handler
        def timeout_handler(signum, frame):
            raise TimeoutError("Code execution timed out")
        
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)  # 5 second timeout
        
        try:
            # Execute the code in restricted environment
            exec(code, safe_environment)
        finally:
            # Restore original state
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
        
        # Return collected output
        return ''.join(output_lines).rstrip('\n') if output_lines else ""
        
    except TimeoutError as e:
        return f"Error: {str(e)}"
    except SyntaxError as e:
        return f"Syntax Error: {str(e)}"
    except NameError as e:
        return f"Name Error: {str(e)} - This function/variable is not available in the restricted environment"
    except ImportError as e:
        return f"Import Error: {str(e)} - This module is not available in the restricted environment"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# Serve the index.html page
@app.route("/")
def index():
    return render_template("index.html")


# Handle the incoming code from the client and send back the output
@socketio.on("code_change")
def handle_code_change(code):
    output = execute_code(code)
    emit("output", {"output": output})


if __name__ == "__main__":
    socketio.run(app, debug=True)
