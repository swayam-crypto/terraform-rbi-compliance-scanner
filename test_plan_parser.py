from compliance_scanner.engine.scan_engine import scan_plan

findings = scan_plan("examples/plans/aws_basic_plan.json")

print(findings)
