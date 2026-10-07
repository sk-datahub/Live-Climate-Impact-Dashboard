import subprocess
import sys
import os


# --------------------------------------------------
# Project folder
# --------------------------------------------------

project_folder = os.path.dirname(
    os.path.abspath(__file__)
)


# --------------------------------------------------
# Run a Python script
# --------------------------------------------------

def run_script(script_name):

    print("\n")
    print("=" * 70)
    print(f"▶ Running: {script_name}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script_name],
        cwd=project_folder
    )

    if result.returncode != 0:

        print(f"\n❌ {script_name} failed!")

        sys.exit(1)

    print(f"\n✅ {script_name} completed successfully!")


# --------------------------------------------------
# Complete Pipeline
# --------------------------------------------------

print("\n")
print("🌍 LIVE CLIMATE DATA PIPELINE")
print("=" * 70)


# Step 1
run_script("weather_api.py")


# Step 2
run_script("air_quality_api.py")


# Step 3
run_script("combine_data.py")


# Step 4
run_script("climate_score.py")


# Step 5
run_script("load_to_mysql.py")


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("\n")
print("=" * 70)
print("🎉 COMPLETE PIPELINE FINISHED!")
print("=" * 70)

print("""
Weather API
     ↓
Air Quality API
     ↓
Combined Data
     ↓
Climate Impact Score
     ↓
MySQL Database
""")

print("✅ New climate data has been collected and stored.")