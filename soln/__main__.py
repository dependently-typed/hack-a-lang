import sys
import os

# Fix imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import Lox

if __name__ == "__main__":
    if len(sys.argv) == 2:
        Lox().runFile(sys.argv[1])
    else:
        sys.exit("Usage: python -m soln <filename>")
