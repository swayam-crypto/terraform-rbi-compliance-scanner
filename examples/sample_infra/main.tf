provider "aws" {
  region = "us-east-1"
}

# VIOLATION: holds customer transaction data but sits outside India,
# and has no encryption configured
resource "aws_s3_bucket" "customer_transactions" {
  bucket = "customer-transaction-records"
  region = "us-east-1"

  tags = {
    data_type = "financial"
    purpose   = "transaction-logs"
  }
}

# COMPLIANT: correctly in Mumbai region with encryption enabled
resource "aws_s3_bucket" "kyc_documents" {
  bucket = "kyc-customer-documents"
  region = "ap-south-1"

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    data_type = "kyc"
    purpose   = "customer-identity-docs"
  }
}

# Unrelated bucket, no sensitive data tags - should not be flagged
resource "aws_s3_bucket" "static_website_assets" {
  bucket = "company-marketing-site"
  region = "us-east-1"

  tags = {
    purpose = "public-assets"
  }
}
