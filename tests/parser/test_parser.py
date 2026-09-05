from compliance_scanner.parser import parse_terraform_directory


def test_parses_sample_infra_directory():
    resources = parse_terraform_directory("examples/sample_infra")
    assert "aws_s3_bucket" in resources
    assert "customer_transactions" in resources["aws_s3_bucket"]

    bucket = resources["aws_s3_bucket"]["customer_transactions"]
    assert bucket["region"] == "us-east-1"
    assert bucket["tags"]["data_type"] == "financial"
