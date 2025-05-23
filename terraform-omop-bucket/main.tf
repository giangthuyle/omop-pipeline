terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.36.1"
    }
    aws = {
      source  = "hashicorp/aws",
      version = "5.98.0"
    }
    fivetran = {
      source  = "fivetran/fivetran"
      version = ">= 1.7.0"
    }
  }
  backend "s3" {
    bucket         = "giang-terraform-states"
    key            = "states"
    region         = "ap-southeast-2"
    use_lockfile   = true
  }
}
provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.google_project_id
  region  = var.google_region
}

provider "fivetran" {}

resource "google_service_account" "bqowner" {
  account_id = "omop-bq-sa"
}

data "google_project" "current_project" {
}
