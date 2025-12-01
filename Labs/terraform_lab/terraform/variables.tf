# Region to deploy into
variable "gcp_region" {
  type    = string
  default = "us-east1"
}

# Project ID - will use gcloud config if not specified
variable "project_id" {
  type        = string
  description = "GCP Project ID (uses gcloud config default if not set)"
  default     = null
}

# Artifact Registry & GKE settings
variable "artifact_registry_name" {
  type    = string
  default = "fastapi-albums"
}

variable "service_name" {
  type    = string
  default = "albums-api"
}

variable "container_port" {
  type    = number
  default = 8080
}

variable "replica_count" {
  type    = number
  default = 2
}