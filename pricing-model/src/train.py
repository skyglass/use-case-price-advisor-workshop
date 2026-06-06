# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/

import os
import pathlib
import numpy as np
import pandas as pd
import tensorflow as tf

# ----------------------------------------------------------------------
# 0.  Convenience: tf.data.Dataset.from_parquet for TF-2.15 (optional)
# ----------------------------------------------------------------------
if not hasattr(tf.data.Dataset, "from_parquet"):
  def _from_parquet(path):
    df = pd.read_parquet(pathlib.Path(path))
    return tf.data.Dataset.from_tensor_slices(dict(df))
  tf.data.Dataset.from_parquet = staticmethod(_from_parquet)

# ----------------------------------------------------------------------
# 1.  Configuration
# ----------------------------------------------------------------------
DATA_DIR = pathlib.Path("data/processed")
EXPORT_DIR = pathlib.Path("data/pricing_saved_model")
NUMERIC   = ["inventory_level", "demand", "competitor_price"]  # 3 columns
EMB_SIZE  = 16
BATCH     = 256
EPOCHS    = 30

# ── scaler constants (force float32 so math matches model input) ──────
mean  = np.load(DATA_DIR / "scaler_mean.npy").astype("float32")
scale = np.load(DATA_DIR / "scaler_scale.npy").astype("float32")

# ----------------------------------------------------------------------
# 2.  Dataset helpers
# ----------------------------------------------------------------------
def make_dataset(split: str) -> tf.data.Dataset:
  """Return batched tf.data.Dataset for 'train' or 'val' parquet file."""
  df_path = DATA_DIR / f"{split}.parquet"
  ds = tf.data.Dataset.from_parquet(str(df_path))

  def to_inputs(row):
    # label as float32
    label = tf.cast(row.pop("price_sold"), tf.float32)
    # product_id as string (usually already tf.string, but this is safe)
    pid = row.pop("product_id")
    pid = tf.cast(pid, tf.string)

    # numeric features in a FIXED order, all cast to float32
    feats = tf.stack(
      [tf.cast(row.pop(c), tf.float32) for c in NUMERIC],
      axis=-1
    )

    return {
             "serving_default_product_id": pid,
             "serving_default_input": feats
           }, label

  ds = ds.map(to_inputs, num_parallel_calls=tf.data.AUTOTUNE)

  if split == "train":
    ds = ds.shuffle(10_000)

  return ds.batch(BATCH).prefetch(tf.data.AUTOTUNE)

# ----------------------------------------------------------------------
# 3.  Build Keras model
# ----------------------------------------------------------------------
def build_model(vocab_ds: tf.data.Dataset) -> tf.keras.Model:
  pid_in   = tf.keras.Input(shape=(1,),           dtype=tf.string,
                            name="serving_default_product_id")
  feats_in = tf.keras.Input(shape=(len(NUMERIC),), dtype=tf.float32,
                            name="serving_default_input")

  lookup = tf.keras.layers.StringLookup()
  lookup.adapt(vocab_ds)
  pid_ids  = lookup(pid_in)
  pid_vecs = tf.keras.layers.Embedding(
    input_dim=lookup.vocabulary_size(), output_dim=EMB_SIZE)(pid_ids)
  pid_vecs = tf.keras.layers.Flatten()(pid_vecs)

  # scale numeric features
  scaled = (feats_in - tf.constant(mean,  dtype=tf.float32)) / \
           tf.constant(scale, dtype=tf.float32)

  x = tf.keras.layers.Concatenate()([pid_vecs, scaled])
  x = tf.keras.layers.Dense(64, activation="relu")(x)
  x = tf.keras.layers.Dense(32, activation="relu")(x)
  out = tf.keras.layers.Dense(1)(x)

  model = tf.keras.Model([pid_in, feats_in], out)
  model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
                loss="mse",
                metrics=[tf.keras.metrics.MeanAbsolutePercentageError()])
  return model

# ----------------------------------------------------------------------
# 4.  Train & export
# ----------------------------------------------------------------------
def main():
  ds_train = make_dataset("train")
  ds_val   = make_dataset("val")
  vocab_ds = tf.data.Dataset.from_parquet(
    str(DATA_DIR / "train.parquet")).map(lambda x: x["product_id"])

  model = build_model(vocab_ds)

  model.fit(
    ds_train,
    validation_data=ds_val,
    epochs=EPOCHS,
    callbacks=[tf.keras.callbacks.EarlyStopping(patience=5,
                                                restore_best_weights=True)]
  )

  # ---- force variable creation with one dummy call ------------------
  dummy_pid   = tf.constant([["dummy"]], dtype=tf.string)
  dummy_feats = tf.constant([[0., 0., 0.]], dtype=tf.float32)
  _ = model([dummy_pid, dummy_feats])

  # ---- define explicit serving signature ---------------------------
  @tf.function(input_signature=[
    tf.TensorSpec([None, 1], tf.string,  name="serving_default_product_id"),
    tf.TensorSpec([None, 3], tf.float32, name="serving_default_input")
  ])
  def serve(pid, feats):
    return {"Identity": model([pid, feats])}

  # ---- export SavedModel (TF-2.15 / Keras-2.15) ---------------------
  tf.keras.models.save_model(
    model,
    EXPORT_DIR,
    overwrite=True,
    save_format="tf",
    signatures={"serving_default": serve}
  )

  print(f"✅ Exported to {EXPORT_DIR}")

# ----------------------------------------------------------------------
if __name__ == "__main__":
  os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"   # friendlier CPU perf on Win
  tf.config.optimizer.set_jit(True)          # optional XLA
  main()
