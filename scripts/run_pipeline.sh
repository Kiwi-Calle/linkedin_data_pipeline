#!/bin/bash

echo "🚀 Welcome to the LinkedIn Ads Data Pipeline! 🚀"
echo ""
read -p "Enter your LinkedIn Ads Account ID: " ACCOUNT_ID
read -p "Enter your Authorization Code: " AUTHORIZATION_CODE
read -p "Enter start date for backfill (YYYY-MM-DD): " START_DATE
read -p "Enter end date for backfill (YYYY-MM-DD): " END_DATE
read -p "Enter your Google Cloud Project ID: " PROJECT_ID
read -p "Enter your BigQuery Dataset Name: " BQ_DATASET
read -p "Enter your BigQuery Table Name: " BQ_TABLE"

echo "Running backfill process now..."
docker run --rm \
  -e ACCOUNT_ID="$ACCOUNT_ID" \
  -e AUTHORIZATION_CODE="$AUTHORIZATION_CODE" \
  -e START_DATE="$START_DATE" \
  -e END_DATE="$END_DATE" \
  -e PROJECT_ID="$PROJECT_ID" \
  -e BQ_DATASET="$BQ_DATASET" \
  -e BQ_TABLE="$BQ_TABLE" \
  gcr.io/$PROJECT_ID/linkedin-ads-pipeline
