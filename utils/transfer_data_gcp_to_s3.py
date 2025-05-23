from google.cloud import bigquery
from google.cloud.bigquery import DatasetReference

PROJECT_ID = "omop-project-460601"
DATASET_ID = "omop"
OMNI_DATASET_ID = "omop_omni"
DATASET_REPLICA_REGION = "aws-us-east-1"
S3_BUCKET = "omop-giang-project"
CONNECTION_ID = "bigquery-omni-aws-connection"
CONNECTION_REGION = "aws-us-east-1"

client= bigquery.Client(project= PROJECT_ID)

def add_replica_in_omni_region(table_name):
    create_replica_sql = f"""
    CREATE OR REPLACE TABLE
        `{PROJECT_ID}.{OMNI_DATASET_ID}.{table_name}`
    AS
    SELECT *
    FROM
        `{PROJECT_ID}.{DATASET_ID}.{table_name}`™£¡
    """
    job = client.query(create_replica_sql)
    job.result()
    print(f"Table {table_name} has been created in omni region")

def list_tables():
    dataset_ref = DatasetReference(project = PROJECT_ID, dataset_id= DATASET_ID)
    tables = client.list_tables(dataset_ref)
    return [table.table_id for table in tables]

def export_table_to_s3(table_name):
    destination_uri = f"s3://{S3_BUCKET}/{table_name}"
    export_sql = f"""
    EXPORT DATA WITH CONNECTION `{CONNECTION_ID}`
    OPTIONS(
        uri='{destination_uri}',
        format='PARQUET'
    )
    AS
    SELECT * FROM `{PROJECT_ID}.{OMNI_DATASET_ID}.{table_name}`
    """

    print(f"Exporting table: {table_name} to {destination_uri}")
    job = client.query(export_sql)
    job.result()
    print(f"Exported table: {table_name}")

def main():
    table_names = list_tables()
    for table_name in table_names:
        try:
            add_replica_in_omni_region(table_name)
            export_table_to_s3(table_name)
        except Exception as e:
            print(f"Failed to export table: {table_name}:{e}")

if __name__ == "__main__":
    main()