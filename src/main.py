import os
import requests
import pandas as pd
from google.cloud import bigquery
from auth import get_access_token

# Get input from environment variables
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
START_DATE = os.getenv("START_DATE")
END_DATE = os.getenv("END_DATE")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")
PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")

def fetch_ads_data():
    """Fetch LinkedIn Ads data using the API"""
    try:
        access_token = get_access_token(AUTHORIZATION_CODE)
        if not access_token:
            raise Exception("Failed to retrieve access token.")

        url = f"https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange=(start:{START_DATE},end:{END_DATE})&accounts=urn:li:sponsoredAccount:{ACCOUNT_ID}"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.json()}")

        data = response.json()
        if "elements" not in data or not data["elements"]:
            raise Exception("No data found in the response.")

        return data["elements"]

    except Exception as e:
        print(f"❌ Error fetching data from LinkedIn API: {e}")
        return None

def upload_to_bigquery(data):
    """Upload fetched data to BigQuery"""
    try:
        if not data:
            raise ValueError("No data to upload to BigQuery.")

        client = bigquery.Client(project=PROJECT_ID)
        table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

        df = pd.DataFrame(data)
        if df.empty:
            raise ValueError("Converted DataFrame is empty. No valid data to upload.")

        job = client.load_table_from_dataframe(df, table_id)
        job.result()

        print(f"✅ Data successfully uploaded to BigQuery table: {BQ_DATASET}.{BQ_TABLE}!")

    except Exception as e:
        print(f"❌ Error uploading data to BigQuery: {e}")

if __name__ == "__main__":
    ads_data = fetch_ads_data()
    if ads_data:
        upload_to_bigquery(ads_data)
    else:
        print("❌ No data retrieved. Skipping upload to BigQuery.")
