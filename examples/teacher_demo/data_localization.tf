# ============================================================
# RBI-001: Data Localization
# RBI Circular DPSS.CO.OD.No.2785/06.08.005/2017-2018 (Apr 2018)
# Financial/customer data must be stored in an Indian AWS region.
# ============================================================

# BAD: holds financial data but is hosted outside India (us-east-1)
resource "aws_s3_bucket" "bad_customer_payments" {
  bucket = "customer-payments-store"
  region = "us-east-1"
  tags = {
    data_type = "financial"
  }
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
}

# GOOD: same kind of data, correctly hosted in Mumbai (ap-south-1)
resource "aws_s3_bucket" "good_customer_payments" {
  bucket = "customer-payments-store-in"
  region = "ap-south-1"
  tags = {
    data_type = "financial"
  }
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
}