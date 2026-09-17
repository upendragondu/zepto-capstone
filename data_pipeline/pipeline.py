import subprocess
import sys


def run_step(script):
    print("\n" + "=" * 60)
    print(f"RUNNING: {script}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script],
        check=True
    )

    return result.returncode


try:

    run_step("data_pipeline/scraper.py")

    run_step("data_pipeline/database.py")

    run_step("data_pipeline/queries.py")

    print("\n" + "=" * 60)
    print("COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
    print("=" * 60)

except subprocess.CalledProcessError as error:

    print("\nPipeline failed.")
    print("Failed step:", error)