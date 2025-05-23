output "bucket_name" {
  value = aws_s3_bucket.omop.id
}

output "bigquery_omni_role" {
  value = aws_iam_role.bq_omni_role.arn
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.omop.dataset_id
}

output "bigquery_connection_id" {
  value = google_bigquery_connection.export_data_connection.connection_id
}