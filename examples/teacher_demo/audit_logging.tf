# ============================================================
# RBI-003: Audit Log Retention (180 days)
# CERT-In Cybersecurity Directions 2022, Direction (iv),
# issued under IT Act Section 70B(6)
# ICT system logs must be retained for at least 180 days.
# ============================================================

# BAD: retention set far below the mandated 180 days
resource "aws_cloudwatch_log_group" "bad_short_retention" {
  name              = "app-logs-short"
  retention_in_days = 30
}

# GOOD: retention meets the 180-day minimum
resource "aws_cloudwatch_log_group" "good_compliant_retention" {
  name              = "app-logs-compliant"
  retention_in_days = 180
}