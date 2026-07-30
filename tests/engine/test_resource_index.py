from compliance_scanner.engine import ResourceIndex
from compliance_scanner.parser.terraform_parser import ResolvedResource


def make_resource(resource_type: str, resource_name: str) -> ResolvedResource:
    return ResolvedResource(
        resource_type=resource_type,
        resource_name=resource_name,
        config={},
        provider_defaults={},
    )


def test_index_preserves_original_resource_order():
    bucket = make_resource("aws_s3_bucket", "transactions")
    log_group = make_resource("aws_cloudwatch_log_group", "audit")
    index = ResourceIndex([bucket, log_group])

    assert len(index) == 2
    assert tuple(index) == (bucket, log_group)
    assert index.resources == (bucket, log_group)
    assert index.resource_types == {"aws_s3_bucket", "aws_cloudwatch_log_group"}


def test_index_looks_up_resources_by_type_name_and_combined_key():
    bucket = make_resource("aws_s3_bucket", "transactions")
    database = make_resource("aws_db_instance", "transactions")
    index = ResourceIndex([bucket, database])

    assert index.of_type("aws_s3_bucket") == (bucket,)
    assert index.of_type("aws_iam_role") == ()
    assert index.named("transactions") == (bucket, database)
    assert index.named("missing") == ()
    assert index.find("aws_db_instance", "transactions") == (database,)
    assert index.find("aws_s3_bucket", "missing") == ()


def test_index_returns_all_matches_for_ambiguous_plan_resources():
    first = make_resource("aws_s3_bucket", "transactions")
    second = make_resource("aws_s3_bucket", "transactions")
    index = ResourceIndex([first, second])

    assert index.find("aws_s3_bucket", "transactions") == (first, second)
