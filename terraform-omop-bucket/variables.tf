variable "aws_region" {
  default = "us-east-1"
}

variable "aws_account_number" {
  default = "686010574434"
}

variable "aws_bq_role_name" {
  default = "BigQueryOmniExportRole"
}

variable "bucket_name" {
  default = "omop-giang-project"
}

variable "environment" {
  default = "dev"
}

variable "google_project_id" {
  default = "omop-project-460601"
}

variable "google_region" {
  default = "us-central1"
}

variable "source_dataset" {
  type = object({
    dataset_id = string
    project_id = string
    tables     = list(string)
    region     = string
  })
  default = {
    dataset_id = "cms_synthetic_patient_data_omop"
    project_id = "bigquery-public-data"
    tables = [
      "care_site", "concept", "concept_ancestor", "concept_class", "concept_relationship",
      "condition_era", "condition_occurrence", "cost", "death", "device_exposure",
      "domain", "dose_era", "drug_era", "drug_exposure", "drug_strength",
      "location", "observation", "observation_period", "payer_plan_period", "person",
      "procedure_occurrence", "provider", "relationship", "vocabulary"
    ]
    region = "us"
  }
}