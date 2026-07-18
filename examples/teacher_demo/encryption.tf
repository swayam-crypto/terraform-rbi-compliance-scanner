# ============================================================
# RBI-002: Encryption at Rest
# RBI Cyber Security Framework (2016) — data protection expectation
# Storage resources must have encryption explicitly configured.
# ============================================================

# BAD: no encryption configuration at all
resource "aws_s3_bucket" "bad_unencrypted_bucket" {
  bucket = "unencrypted-data"
  region = "ap-south-1"
}

# GOOD: encryption explicitly enabled
resource "aws_s3_bucket" "good_encrypted_bucket" {
  bucket = "encrypted-data"
  region = "ap-south-1"

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
}