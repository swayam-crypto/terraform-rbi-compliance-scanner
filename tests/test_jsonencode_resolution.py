import textwrap

from compliance_scanner.engine.scan_engine import scan_directory


def test_jsonencode_resolution(tmp_path):
    """
    Regression test for jsonencode() support.

    Ensures that:
    1. jsonencode() policies are parsed correctly.
    2. Allow wildcard policies trigger RBI-005.
    3. Deny wildcard policies are ignored.
    """

    tf = tmp_path / "main.tf"

    tf.write_text(textwrap.dedent("""
            resource "aws_iam_policy" "allow_policy" {
              name = "allow-policy"

              policy = jsonencode({
                Version = "2012-10-17"

                Statement = [{
                  Effect   = "Allow"
                  Action   = "*"
                  Resource = "*"
                }]
              })
            }

            resource "aws_iam_policy" "deny_policy" {
              name = "deny-policy"

              policy = jsonencode({
                Version = "2012-10-17"

                Statement = [{
                  Effect   = "Deny"
                  Action   = "*"
                  Resource = "*"
                }]
              })
            }
            """))

    findings = scan_directory(str(tmp_path))

    # Only the Allow policy should trigger RBI-005
    assert len(findings) == 1

    finding = findings[0]

    assert finding.rule_id == "RBI-005"
    assert finding.resource_type == "aws_iam_policy"
    assert finding.resource_name == "allow_policy"
