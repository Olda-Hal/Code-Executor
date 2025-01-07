import os
import sys
from io import StringIO

def main():
    code = os.environ.get('CODE', '')
    input_data = os.environ.get('INPUT', '')
    
    if input_data:
        sys.stdin = StringIO(input_data)
    
    try:
        exec_globals = {
            '__name__': '__main__',
            '__file__': 'user_code.py',
        }
        exec(code, exec_globals)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()