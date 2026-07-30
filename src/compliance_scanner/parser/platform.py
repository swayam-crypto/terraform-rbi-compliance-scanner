from enum import Enum


class Platform(Enum):
    TERRAFORM = "terraform"
    CLOUDFORMATION = "cloudformation"
    PULUMI = "pulumi"
    BICEP = "bicep"
    KUBERNETES = "kubernetes"
