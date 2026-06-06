# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/

import tensorflow as tf

def main():

  pid = "iphone-15-pro"
  inventory_level = 0
  demand = 0
  competitor_price = 0


  model = tf.saved_model.load("data/pricing_saved_model")
  infer = model.signatures["serving_default"]

  product_id = tf.constant([[pid]])  # shape [1, 1]
  raw_features = tf.constant([[inventory_level, demand, competitor_price]], dtype=tf.float32)  # shape [1, 3]

  result = infer(
    serving_default_product_id=product_id,
    serving_default_input=raw_features
  )

  # Show available keys
  print("Output keys:", list(result.keys()))

  # Safely extract the only value (should be the price prediction)
  price = float(next(iter(result.values())).numpy()[0][0])
  print(f"✅ Prediction OK! Price = {price:.2f}")

if __name__ == "__main__":
  main()
