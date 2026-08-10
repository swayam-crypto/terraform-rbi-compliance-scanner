"""Baseline v0.8 controls shared by RBI, DPDP, CERT-In, and CIS mappings."""

from .controls import ComplianceControl, FrameworkMapping


def baseline_control(
    control_id: str,
    title: str,
    category: str,
    severity: str,
    remediation: str,
) -> ComplianceControl:
    return ComplianceControl(
        control_id=control_id,
        title=title,
        category=category,
        severity=severity,
        remediation=remediation,
        framework_mappings=(
            FrameworkMapping("RBI", "Cybersecurity control", "RBI Cyber Security Framework for Banks (2016)"),
            FrameworkMapping("DPDP", "Reasonable security safeguards", "DPDP Act 2023, Section 8(5)"),
            FrameworkMapping("CIS", "Secure configuration", "CIS cloud provider benchmark guidance"),
        ),
    )


DATABASE_BACKUPS = baseline_control("CCIP-BACKUP-RETENTION-001", "Databases must retain backups", "backup_recovery", "high", "Configure an approved backup retention period of at least seven days.")
STORAGE_VERSIONING = baseline_control("CCIP-STORAGE-VERSIONING-001", "Object storage must retain versions", "backup_recovery", "medium", "Enable object versioning to support recovery from deletion and overwrite.")
KMS_ROTATION = baseline_control("CCIP-KEY-ROTATION-001", "Encryption keys must rotate", "cryptography", "medium", "Enable automatic rotation for customer-managed encryption keys.")
DATABASE_DELETION_PROTECTION = baseline_control("CCIP-DATABASE-RECOVERY-001", "Databases must prevent accidental deletion", "backup_recovery", "high", "Enable deletion protection for production database resources.")
DATABASE_MULTI_AZ = baseline_control("CCIP-DATABASE-AVAILABILITY-001", "Databases must be highly available", "availability", "medium", "Enable multi-zone deployment where required by the workload availability policy.")
STORAGE_ACCESS_LOGGING = baseline_control("CCIP-STORAGE-LOGGING-001", "Object storage must record access", "logging_monitoring", "medium", "Enable access logging and send logs to a protected destination.")
LOG_ENCRYPTION = baseline_control("CCIP-LOG-ENCRYPTION-001", "Logs must be encrypted", "data_protection", "medium", "Encrypt log storage with an approved key.")
FUNCTION_VPC = baseline_control("CCIP-FUNCTION-NETWORK-001", "Sensitive functions must use private networking", "network_security", "high", "Attach the function to approved private subnets and security groups.")
VOLUME_ENCRYPTION = baseline_control("CCIP-VOLUME-ENCRYPTION-001", "Block volumes must be encrypted", "data_protection", "high", "Enable encryption at rest for block storage.")
FILE_ENCRYPTION = baseline_control("CCIP-FILE-ENCRYPTION-001", "File systems must be encrypted", "data_protection", "high", "Enable encryption at rest for file storage.")
QUEUE_ENCRYPTION = baseline_control("CCIP-QUEUE-ENCRYPTION-001", "Message queues must be encrypted", "data_protection", "high", "Configure server-side encryption for the message queue.")
TOPIC_ENCRYPTION = baseline_control("CCIP-TOPIC-ENCRYPTION-001", "Notification topics must be encrypted", "data_protection", "high", "Configure server-side encryption for the notification topic.")
SSH_RESTRICTED = baseline_control("CCIP-SSH-RESTRICTION-001", "SSH must not be publicly exposed", "network_security", "critical", "Restrict TCP port 22 ingress to approved administrative networks.")
RDP_RESTRICTED = baseline_control("CCIP-RDP-RESTRICTION-001", "RDP must not be publicly exposed", "network_security", "critical", "Restrict TCP port 3389 ingress to approved administrative networks.")
UNRESTRICTED_INGRESS = baseline_control("CCIP-UNRESTRICTED-INGRESS-001", "Network ingress must not allow all ports from the internet", "network_security", "critical", "Replace unrestricted public ingress with the minimum approved ports and CIDRs.")
