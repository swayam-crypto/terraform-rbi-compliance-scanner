from src.compliance_scanner.parser.suppressions import extract_suppressions, is_suppressed


def _write_tf(path, content):
    with open(path, "w") as f:
        f.write(content)


def test_extracts_single_rule_suppression(tmp_path):
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, '''
# rbi-scan:ignore RBI-001 reason="internal logs, not customer data"
resource "aws_s3_bucket" "internal_logs" {
  bucket = "internal-logs"
}
''')
    suppressions = extract_suppressions(str(tf_file))
    assert ("aws_s3_bucket", "internal_logs") in suppressions
    entry = suppressions[("aws_s3_bucket", "internal_logs")]
    assert entry["all"] is False
    assert "RBI-001" in entry["rules"]
    assert entry["reasons"]["RBI-001"] == "internal logs, not customer data"


def test_extracts_ignore_all(tmp_path):
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, '''
# rbi-scan:ignore-all reason="legacy resource, migration planned Q3"
resource "aws_s3_bucket" "old_bucket" {
  bucket = "old-bucket"
}
''')
    suppressions = extract_suppressions(str(tf_file))
    entry = suppressions[("aws_s3_bucket", "old_bucket")]
    assert entry["all"] is True


def test_suppression_does_not_apply_to_unrelated_resource(tmp_path):
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, '''
# rbi-scan:ignore RBI-001 reason="test"
resource "aws_s3_bucket" "bucket_a" {
  bucket = "a"
}

resource "aws_s3_bucket" "bucket_b" {
  bucket = "b"
}
''')
    suppressions = extract_suppressions(str(tf_file))
    assert ("aws_s3_bucket", "bucket_a") in suppressions
    assert ("aws_s3_bucket", "bucket_b") not in suppressions


def test_no_suppressions_when_none_present(tmp_path):
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, '''
resource "aws_s3_bucket" "plain_bucket" {
  bucket = "plain"
}
''')
    suppressions = extract_suppressions(str(tf_file))
    assert suppressions == {}


def test_is_suppressed_helper():
    suppressions = {
        ("aws_s3_bucket", "bucket_a"): {"all": False, "rules": {"RBI-001"}, "reasons": {}}
    }
    assert is_suppressed("RBI-001", "aws_s3_bucket", "bucket_a", suppressions) is True
    assert is_suppressed("RBI-002", "aws_s3_bucket", "bucket_a", suppressions) is False
    assert is_suppressed("RBI-001", "aws_s3_bucket", "bucket_c", suppressions) is False


def test_code_between_comment_and_resource_breaks_suppression(tmp_path):
    """A suppression comment only applies if nothing but comments/blank lines
    separate it from the resource block it's meant to cover."""
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, '''
# rbi-scan:ignore RBI-001 reason="test"
variable "unrelated" {
  type = string
}

resource "aws_s3_bucket" "bucket_a" {
  bucket = "a"
}
''')
    suppressions = extract_suppressions(str(tf_file))
    assert ("aws_s3_bucket", "bucket_a") not in suppressions