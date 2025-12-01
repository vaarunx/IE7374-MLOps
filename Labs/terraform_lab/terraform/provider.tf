# Specify where to find the GCP provider
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

# Get GCP config (access token only)
data "google_client_config" "default" {}

# Configure GCP credentials & region
provider "google" {
  project = "ie7374-475102"  
  region  = var.gcp_region
}

# Configure Docker provider to authenticate against Artifact Registry
provider "docker" {
  registry_auth {
    address  = "${var.gcp_region}-docker.pkg.dev"
    username = "oauth2accesstoken"
    password = data.google_client_config.default.access_token
  }
}