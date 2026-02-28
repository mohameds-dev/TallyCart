#!/bin/bash

# Download default CSV from Google Sheets
# This script downloads the receipts_data CSV from the shared Google Sheet

GOOGLE_SHEET_ID="1swHtHTNIqwcZaIplDUuNRqmMMllI_GyelsN0RsB-FEo"
CSV_URL="https://docs.google.com/spreadsheets/d/${GOOGLE_SHEET_ID}/export?format=csv&gid=0"
OUTPUT_DIR="data"
OUTPUT_FILE="${OUTPUT_DIR}/receipts_data.csv"

# Create data directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

# Download the CSV
echo "Downloading default CSV from Google Sheets..."
if wget --no-check-certificate -q "${CSV_URL}" -O "${OUTPUT_FILE}"; then
    echo "✅ Successfully downloaded CSV to ${OUTPUT_FILE}"
    exit 0
else
    echo "❌ Failed to download CSV"
    exit 1
fi

