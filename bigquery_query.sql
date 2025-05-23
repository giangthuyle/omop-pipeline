EXPORT DATA WITH CONNECTION `aws-us-east-1.bigquery-omni-aws-connection`
OPTIONS(uri="s3://omop-giang-project/exports/*", format="PARQUET")
AS SELECT * FROM `omop-project-460601.care_site_demo.care_site` LIMIT 1