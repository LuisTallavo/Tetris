#!/usr/bin/env python3
"""
Run Tetris in the browser.
This script starts the pygbag server and opens the game in your default browser.
"""

import subprocess
import webbrowser
import time
import sys
import os

def main():
    port = 3000
    project_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Starting Tetris server on port {port}...")
    print(f"Project directory: {project_dir}")

    # Start pygbag server
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pygbag", "--port", str(port), project_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except FileNotFoundError:
        print("Error: pygbag not installed. Install it with: pip install pygbag")
        sys.exit(1)

    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)

    # Open browser
    url = f"http://localhost:{port}"
    print(f"Opening {url} in your browser...")
    webbrowser.open(url)

    print("Game is running! Press Ctrl+C to stop the server.")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        process.terminate()
        process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main()
