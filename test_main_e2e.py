"""Test main.py end-to-end pipeline."""

import sys
from io import StringIO

# Simulate user input
test_input = "a\nac\n"  # regex: "a", scan: "ac"
sys.stdin = StringIO(test_input)

# Capture output
old_stdout = sys.stdout
sys.stdout = StringIO()

try:
    from main import main
    main()
    output = sys.stdout.getvalue()
finally:
    sys.stdout = old_stdout

print("=== OUTPUT ===")
print(output)
