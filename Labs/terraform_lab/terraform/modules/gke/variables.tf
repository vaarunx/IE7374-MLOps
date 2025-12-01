variable "service_name" {
  type        = string
  description = "Base name for GKE resources"
}

variable "network_name" {
  type        = string
  description = "VPC network name"
}

variable "subnetwork_name" {
  type        = string
  description = "Subnet name"
}

variable "region" {
  type        = string
  description = "GCP region"
}