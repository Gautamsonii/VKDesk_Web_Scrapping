import time
from concurrent.futures import ThreadPoolExecutor
import subprocess

def run_scraper(script):
    try:
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

if __name__ == "__main__":
    scripts = ["ajax.py", "forms.py", "advanced.py", ]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_scraper, scripts)

    end_time = time.time()
    print(f"Scraping completed in {end_time - start_time} seconds.")
