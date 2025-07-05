#!/usr/bin/env python3

import subprocess
import sys

def ask_gemini(prompt):
    """Execute gemini-cli with the given prompt and return the result."""
    cmd = ["npx", "--yes", "https://github.com/google-gemini/gemini-cli", "-p", prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ask_gemini.py <question>")
        sys.exit(1)
    
    question = sys.argv[1]
    response = ask_gemini(question)
    print(response)
