resource "fivetran_group" "omop" {
  name = "OmopBQtoS3"
}

# resource "fivetran_destination" "destination" {
#   group_id         = fivetran_group.omop.id
#   region           = var.aws_region
#   service          = "new_s3_datalake"
#   time_zone_offset = ""
#
#   config {
#     auth_type             = ""
#     aws_access_key_id     = ""
#     aws_secret_access_key = ""
#     bucket                = var.bucket_name
#   }
# }
#
# resource "fivetran_connector" "bigquery_connector" {
#   group_id = fivetran_group.omop.id
#   service  = ""
# }