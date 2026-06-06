# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/

from confluent_kafka import Producer
import pathlib
import os

# --- Config ---
BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC  = os.getenv("KAFKA_TOPIC", "ml-model")
ZIP_FILE = pathlib.Path("data/pricing_saved_model.zip")

# --- Load model as bytes ---
if not ZIP_FILE.exists():
  raise FileNotFoundError(f"Model artifact not found: {ZIP_FILE}")

with open(ZIP_FILE, "rb") as f:
  payload = f.read()

# --- Set up Kafka producer ---
producer = Producer({"bootstrap.servers": BROKER})

# --- Send it (async) ---
producer.produce(
  TOPIC,
  value=payload,
  key="pricing-model"
)

producer.flush()
print(f"✅ Sent {ZIP_FILE.name} to Kafka topic '{TOPIC}' via broker '{BROKER}'")