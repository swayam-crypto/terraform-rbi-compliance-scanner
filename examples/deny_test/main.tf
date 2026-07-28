resource "aws_iam_policy" "deny_policy" {
  name = "deny-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Deny"
      Action = "*"
      Resource = "*"
    }]
  })
}