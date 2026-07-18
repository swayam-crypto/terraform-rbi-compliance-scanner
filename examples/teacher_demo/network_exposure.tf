# ============================================================
# RBI-004: Network Exposure
# RBI Cyber Security Framework (2016) access controls +
# DPDPA 2023 Section 8(5) reasonable security safeguards
# Resources holding sensitive data must not be publicly accessible.
# ============================================================

# BAD: customer data bucket is publicly readable
resource "aws_s3_bucket" "bad_public_customer_data" {
  bucket = "customer-data-exposed"
  region = "ap-south-1"
  acl    = "public-read"
  tags = {
    data_type = "customer"
  }
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
}

# GOOD: same kind of data, kept private
resource "aws_s3_bucket" "good_private_customer_data" {
  bucket = "customer-data-secured"
  region = "ap-south-1"
  acl    = "private"
  tags = {
    data_type = "customer"
  }
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
}