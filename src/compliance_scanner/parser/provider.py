from enum import Enum


class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    OCI = "oci"
    DIGITALOCEAN = "digitalocean"
    CLOUDFLARE = "cloudflare"
