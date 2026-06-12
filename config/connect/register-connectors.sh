#!/bin/sh
set -eu

CONNECT_URL="${CONNECT_URL:-http://kafka-connect:8083}"

echo "Waiting for Kafka Connect at ${CONNECT_URL}..."
until curl -fsS "${CONNECT_URL}/connectors" >/dev/null; do
  sleep 2
done

for connector in /connect/*-outbox.json; do
  echo "Registering ${connector}..."
  curl -fsS -X POST "${CONNECT_URL}/connectors" \
    -H "Content-Type: application/json" \
    --data-binary @"${connector}" || true
done

echo "Registered connectors:"
curl -fsS "${CONNECT_URL}/connectors"
