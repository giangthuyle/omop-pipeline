from google.cloud import bigquery
import pyarrow as pa
import pyarrow.parquet as pq
import os
import boto3


PROJECT_ID = "gsla-omop-project"
DATASET_ID = "bigquery-public-data.cms_synthetic_patient_data_omop"
TABLES = [
    "care_site", "concept", "concept_ancestor", "concept_class", "concept_relationship",
    "condition_era", "condition_occurrence", "cost", "death", "device_exposure",
    "domain", "dose_era", "drug_era", "drug_exposure", "drug_strength",
    "location", "observation", "observation_period", "payer_plan_period", "person",
    "procedure_occurrence", "provider", "relationship", "vocabulary"
]
LIMIT = 5000
OUTPUT_DIR = "./data/parquet"
BUCKET_NAME = "omop-project"
S3_PREFIX = "omop-parquet"

os.makedirs(OUTPUT_DIR, exist_ok=True)

client = bigquery.Client()
s3 = boto3.client("s3")

def download_sample():
    for table in TABLES:
        query = f"""
        SELECT * 
        FROM `{DATASET_ID}.{table}` 
        LIMIT {LIMIT}
        """
        df = client.query(query).to_dataframe()
        table_path = os.path.join(OUTPUT_DIR, f"{table}.parquet")
        table_pa = pa.Table.from_pandas(df)
        pq.write_table(table_pa, table_path)
        print(f"Downloaded {table}: {len(df)} rows → {table_path}")

def upload_folder(local_dir, bucket_name, s3_prefix):
    for root, dirs, files in os.walk(local_dir):
        for filename in files:
            if filename.endswith(".parquet"):
                local_path = os.path.join(root, filename)
                s3_key = os.path.join(f"{s3_prefix}/{filename}")
                s3.upload_file(local_path, bucket_name, s3_key)
                print(f"Uploaded {filename} to s3://{bucket_name}/{s3_key}")

def main():
    # download_sample()
    upload_folder(local_dir=OUTPUT_DIR, bucket_name=BUCKET_NAME, s3_prefix=S3_PREFIX)

if __name__ == "__main__":
    main()
