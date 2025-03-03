import subprocess
import os
from dotenv import load_dotenv

def api_call():
    """Runs the GEMINI API call script on list of items"""
    print("Running API call")
    subprocess.run(["python", "gemini_api_call.py"], check=True)

if __name__ == "__main__":
    try:
        print("Running job pipeline...")
        api_call()
        print("Pipeline completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed with error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")