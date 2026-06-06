#!/bin/bash
set -e

echo "Step 1: Make datasets"
python src/make_dataset.py

echo "Step 2: Train the model"
python src/train.py

echo "Step 3: Test the model"
python src/sanity_test.py

echo "Compress the model to zip"
python src/export_savedmodel.py

echo "Send zip bytes to kafka"
#docker-compose up -d
python src/send_model_to_kafka.py