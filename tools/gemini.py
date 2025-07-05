#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def ask_gemini(prompt, kb_dir):
    """Execute gemini-cli with the given prompt and kb directory context."""
    # Change to the kb directory for context
    kb_path = Path(__file__).parent.parent / "kb" / kb_dir
    
    # Execute gemini-cli from the kb directory
    cmd = ["npx", "--yes", "https://github.com/google-gemini/gemini-cli", "-p", prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=str(kb_path))
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/gemini.py <docs|dolphie|harlequin|posting> <question>")
        sys.exit(1)
    
    kb_dir = sys.argv[1]
    question = sys.argv[2]
    
    valid_dirs = ['docs', 'dolphie', 'harlequin', 'posting']
    if kb_dir not in valid_dirs:
        print(f"Error: Invalid kb directory. Must be one of: {', '.join(valid_dirs)}")
        sys.exit(1)
    
    response = ask_gemini(question, kb_dir)
    print(response)

if __name__ == "__main__":
    main()