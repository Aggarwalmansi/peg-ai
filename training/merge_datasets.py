import pandas as pd
import os
from pathlib import Path
import logging

# setup logging
logging.basicConfig(level=logging.INFO)

INPUT_FOLDER = Path("data/interim")
OUTPUT_FILE = Path("data/processed/guardian_dataset.csv")

datasets = []

csv_files = sorted(INPUT_FOLDER.glob("*.csv"))

if not csv_files:
    raise ValueError("No CSV files found in data/interim")

for file in csv_files:
    try:
        logging.info(f"Loading {file.name}")
        df = pd.read_csv(file)

        datasets.append(df)

    except Exception as e:
        logging.warning(f"Skipping {file.name}: {e}")

combined = pd.concat(datasets, ignore_index=True)

before = len(combined)

combined = combined.drop_duplicates()

after = len(combined)

logging.info(f"Removed {before - after} duplicates")
logging.info(f"Final dataset size: {after}")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

combined.to_csv(OUTPUT_FILE, index=False)

logging.info(f"Saved dataset to {OUTPUT_FILE}")