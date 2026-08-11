data "aws_caller_identity" "current" {}

# 1. S3 Bucket for Raw Documentation
resource "aws_s3_bucket" "docs_bucket" {
  bucket        = "enterprise-internal-docs-secure-repo-2026"
  force_destroy = true
}

# 2. IAM Role for Bedrock Knowledge Base
resource "aws_iam_role" "bedrock_kb_role" {
  name = "AmazonBedrockExecutionRoleForKB2026"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "bedrock.amazonaws.com"
      }
    }]
  })
}

# IAM Policy for Bedrock Role to Access S3 Data Source
resource "aws_iam_role_policy" "bedrock_kb_s3_policy" {
  name = "BedrockKBS3Policy"
  role = aws_iam_role.bedrock_kb_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.docs_bucket.arn,
          "${aws_s3_bucket.docs_bucket.arn}/*"
        ]
      }
    ]
  })
}

# Output the required identifiers for application integration
output "knowledge_base_bucket" {
  value       = aws_s3_bucket.docs_bucket.id
  description = "S3 Bucket for storing internal documentation documents"
}