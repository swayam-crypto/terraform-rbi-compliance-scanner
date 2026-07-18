# ============================================================
# RBI-005: Least Privilege (IAM)
# RBI Cyber Security Framework (2016) — Access Control principle
# IAM policies must not grant wildcard (*) actions or resources.
# ============================================================

# BAD: wildcard action AND wildcard resource — full, unrestricted access
resource "aws_iam_policy" "bad_wildcard_policy" {
  name   = "overly-broad-policy"
  policy = "{\"Statement\": [{\"Effect\": \"Allow\", \"Action\": \"*\", \"Resource\": \"*\"}]}"
}

# GOOD: scoped to a specific action and a specific resource
resource "aws_iam_policy" "good_scoped_policy" {
  name   = "scoped-read-only-policy"
  policy = "{\"Statement\": [{\"Effect\": \"Allow\", \"Action\": \"s3:GetObject\", \"Resource\": \"arn:aws:s3:::customer-data-secured/*\"}]}"
}