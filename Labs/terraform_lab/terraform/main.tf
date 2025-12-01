# Get current GCP project from gcloud config
data "google_project" "current" {
  project_id = data.google_client_config.default.project
}

# Enable required APIs first
resource "google_project_service" "container" {
  project            = data.google_project.current.project_id
  service            = "container.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute" {
  project            = data.google_project.current.project_id
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry" {
  project            = data.google_project.current.project_id
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# Wire together three focused modules: network, artifact_registry, gke

module "network" {
  source         = "./modules/network"
  service_name   = var.service_name
  region         = var.gcp_region
  
  depends_on = [google_project_service.compute]
}

module "artifact_registry" {
  source          = "./modules/artifact_registry"
  repository_name = var.artifact_registry_name
  region          = var.gcp_region
  
  depends_on = [google_project_service.artifactregistry]
}

module "gke" {
  source          = "./modules/gke"
  service_name    = var.service_name
  network_name    = module.network.network_name
  subnetwork_name = module.network.subnetwork_name
  region          = var.gcp_region
  
  depends_on = [google_project_service.container]
}

# Build & push the FastAPI app image into Artifact Registry (AMD64 for GKE)
resource "docker_image" "app" {
  name = "${module.artifact_registry.repository_url}/albums-api:latest"

  build {
    context    = "../"
    dockerfile = "Dockerfile"
    platform   = "linux/amd64"
  }
}

resource "docker_registry_image" "app" {
  name = docker_image.app.name
  
  depends_on = [module.artifact_registry]
}