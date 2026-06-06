# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/

import numpy as np
import pandas as pd
import pathlib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RAW_DIR = pathlib.Path("data/raw")
OUT_DIR = pathlib.Path("data/processed")
NUMERIC = ["inventory_level", "demand", "competitor_price"]
TARGET = "price_sold"


def load_all_csv() -> pd.DataFrame:
  frames = []
  for csv in RAW_DIR.glob("*.csv"):
    frames.append(pd.read_csv(csv))
  if not frames:
    raise SystemExit(f"No CSV files found in {RAW_DIR}")
  return pd.concat(frames, ignore_index=True)


def main():
  OUT_DIR.mkdir(parents=True, exist_ok=True)
  df = load_all_csv()
  # --- very basic cleaning ---
  df = df.dropna(subset=NUMERIC + ["product_id", TARGET])

  # Train / val / test split
  train, test = train_test_split(df, test_size=0.1, random_state=42,
                                 stratify=df["product_id"])
  train, val = train_test_split(train, test_size=0.2, random_state=42,
                                stratify=train["product_id"])

  # Standard-scale numeric columns
  scaler = StandardScaler().fit(train[NUMERIC])
  # for split in (train, val, test):
  #   split[NUMERIC] = scaler.transform(split[NUMERIC])

  # Save to Parquet (compact, typed)
  train.to_parquet(OUT_DIR / "train.parquet", index=False)
  val.to_parquet(OUT_DIR / "val.parquet", index=False)
  test.to_parquet(OUT_DIR / "test.parquet", index=False)
  np.save(OUT_DIR / "scaler_mean.npy", scaler.mean_)
  np.save(OUT_DIR / "scaler_scale.npy", scaler.scale_)


if __name__ == "__main__":
  main()
