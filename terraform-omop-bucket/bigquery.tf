resource "google_bigquery_connection" "export_data_connection" {
  connection_id = "bigquery-omni-aws-connection"
  friendly_name = "bq-s3-export"

  location = "aws-${var.aws_region}"
  aws {
    access_role {
      iam_role_id = "arn:aws:iam::${var.aws_account_number}:role/${var.aws_bq_role_name}"
    }
  }
}

resource "google_bigquery_dataset" "omop" {
  dataset_id                  = "omop"
  location                    = var.source_dataset.region
  default_table_expiration_ms = 108000000 # 3 hours

  access {
    role          = "OWNER"
    user_by_email = google_service_account.bqowner.email
  }
}

resource "google_bigquery_data_transfer_config" "query_config" {
  for_each     = toset(var.source_dataset.tables)
  location     = var.source_dataset.region
  display_name = "Copy ${each.key} table from public dataset"

  data_source_id = "scheduled_query"

  params = {
    query                           = "SELECT * FROM `${var.source_dataset.project_id}.${var.source_dataset.dataset_id}.${each.key}`"
    destination_table_name_template = each.key
    write_disposition               = "WRITE_TRUNCATE"
  }

  schedule = "every monday 09:00"

  destination_dataset_id = google_bigquery_dataset.omop.dataset_id
}