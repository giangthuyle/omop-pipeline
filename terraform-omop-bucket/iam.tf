resource "aws_iam_role" "bq_omni_role" {
  name                 = var.aws_bq_role_name
  max_session_duration = 43200

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "accounts.google.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "accounts.google.com:sub" = "${google_bigquery_connection.export_data_connection.aws[0].access_role[0].identity}"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "bq_omni_export_only_policy" {
  name = "BigQueryOnmiExportPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "BucketLevelAccess"
        Action = [
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.omop.arn
        ]
      },
      {
        Sid = "ObjectLevelAccess"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.omop.arn,
          "${aws_s3_bucket.omop.arn}/*"
        ]
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bg_omni_export_attachment" {
  policy_arn = aws_iam_policy.bq_omni_export_only_policy.arn
  role       = aws_iam_role.bq_omni_role.name
}

resource "aws_iam_role" "fivetran_to_s3" {
  name                 = "FivetranS3Role"
  max_session_duration = 43200

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "accounts.google.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "accounts.google.com:sub" = "${google_bigquery_connection.export_data_connection.aws[0].access_role[0].identity}"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "fivetran_to_s3" {
  name = "FivetranStoreDataInS3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowListBucketOfASpecificPrefix"
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.omop.arn
        ]
      },
      {
        Sid    = "AllowAllObjectActionsInSpecificPrefix"
        Effect = "Allow"
        Action = [
          "s3:DeleteObjectTagging",
          "s3:ReplicateObject",
          "s3:PutObject",
          "s3:GetObjectAcl",
          "s3:GetObject",
          "s3:DeleteObjectVersion",
          "s3:PutObjectTagging",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          aws_s3_bucket.omop.arn,
          "${aws_s3_bucket.omop.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "fivetran_to_s3" {
  policy_arn = aws_iam_policy.fivetran_to_s3.arn
  role       = aws_iam_role.fivetran_to_s3.name
}