#!/usr/bin/env python3
"""
Quack tool - plays the quack.mp3 sound file
"""
import os, sys, subprocess
from pathlib import Path

def play_quack():
    """Play the quack.mp3 file"""
    # Get the project root (parent of tools directory)
    tools_dir = Path(__file__).parent
    project_root = tools_dir.parent
    audio_file = project_root / "assets" / "quack.mp3"
    
    if not audio_file.exists():
        print(f"Error: Audio file not found at {audio_file}")
        return 1
    
    # Try different audio players based on platform
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", str(audio_file)], check=True)
        elif sys.platform.startswith("linux"):  # Linux
            # Try common Linux audio players
            for player in ["paplay", "aplay", "mpg123", "ffplay"]:
                if subprocess.run(["which", player], capture_output=True).returncode == 0:
                    subprocess.run([player, str(audio_file)], check=True)
                    break
            else:
                print("Error: No suitable audio player found on Linux")
                return 1
        elif sys.platform == "win32":  # Windows
            os.startfile(str(audio_file))
        else:
            print(f"Error: Unsupported platform {sys.platform}")
            return 1
            
        print("Quack! 🦆")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(play_quack())