provider "aws" {
  region = "ap-south-1"
}

# COMPLIANT: correct region, encrypted, all rules satisfied
resource "aws_s3_bucket" "customer_records" {
  bucket = "customer-records-store"
  region = "ap-south-1"
  acl    = "private"

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    data_type = "financial"
    purpose   = "customer-records"
  }
}

resource "aws_db_instance" "payments_db" {
  region              = "ap-south-1"
  storage_encrypted   = true
  publicly_accessible = false

  tags = {
    data_type = "payment"
  }
}

resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "app-logs"
  retention_in_days = 180
}
