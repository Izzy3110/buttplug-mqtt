import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv('.env')


def restart_program():
    """Restarts the main script when it fails."""
    while True:
        try:
            # Run the main script
            result = subprocess.call([
                os.getenv('PY_EXECUTABLE'),
                "backend.py"])
            if result != 0:  # Check for non-zero return code
                print("Program crashed. Restarting in 5 seconds...")
                time.sleep(5)  # Optional delay before restarting
        except KeyboardInterrupt:
            print("Terminating monitor...")
            break


if __name__ == "__main__":
    restart_program()
