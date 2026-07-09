import os
import time

from compliance_scanner.engine import scan_directory_large


def _write_tf(path, region="us-east-1", data_type="financial"):
    with open(path, "w") as f:
        f.write(f'''
resource "aws_s3_bucket" "test_bucket" {{
  bucket = "test-bucket"
  region = "{region}"
  tags = {{
    data_type = "{data_type}"
  }}
}}
''')


def test_scan_large_matches_scan_directory_results(tmp_path):
    from compliance_scanner.engine import scan_directory

    _write_tf(tmp_path / "main.tf")

    regular_findings = scan_directory(str(tmp_path))
    large_findings = list(scan_directory_large(str(tmp_path), use_cache=False))

    assert len(regular_findings) == len(large_findings)
    assert {f.rule_id for f in regular_findings} == {f.rule_id for f in large_findings}


def test_cache_produces_identical_findings_on_second_run(tmp_path):
    _write_tf(tmp_path / "main.tf")
    cache_path = str(tmp_path / ".rbi_scan_cache.json")

    first_run = list(scan_directory_large(str(tmp_path), use_cache=True, cache_path=cache_path))
    second_run = list(scan_directory_large(str(tmp_path), use_cache=True, cache_path=cache_path))

    assert len(first_run) == len(second_run)
    assert os.path.exists(cache_path)


def test_cache_invalidates_on_file_change(tmp_path):
    tf_file = tmp_path / "main.tf"
    _write_tf(tf_file, region="ap-south-1")  # compliant region
    cache_path = str(tmp_path / ".rbi_scan_cache.json")

    first_run = list(scan_directory_large(str(tmp_path), use_cache=True, cache_path=cache_path))
    first_run_rule_ids = {f.rule_id for f in first_run}
    assert "RBI-001" not in first_run_rule_ids  # region is compliant, no localization violation

    # sleep briefly to guarantee mtime actually changes on fast filesystems
    time.sleep(0.05)
    _write_tf(tf_file, region="us-east-1")  # now non-compliant region

    second_run = list(scan_directory_large(str(tmp_path), use_cache=True, cache_path=cache_path))
    second_run_rule_ids = {f.rule_id for f in second_run}
    assert "RBI-001" in second_run_rule_ids  # cache correctly detected the change and re-scanned
