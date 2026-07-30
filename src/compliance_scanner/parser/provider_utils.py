from compliance_scanner.models.provider import CloudProvider


def infer_provider(resource_type: str) -> CloudProvider:
    if resource_type.startswith("aws_"):
        return CloudProvider.AWS

    if resource_type.startswith("azurerm_"):
        return CloudProvider.AZURE

    if resource_type.startswith(("google_", "google-beta_")):
        return CloudProvider.GCP

    if resource_type.startswith("oci_"):
        return CloudProvider.OCI

    if resource_type.startswith("cloudflare_"):
        return CloudProvider.CLOUDFLARE

    raise ValueError(f"Unsupported provider for resource type: {resource_type}")
