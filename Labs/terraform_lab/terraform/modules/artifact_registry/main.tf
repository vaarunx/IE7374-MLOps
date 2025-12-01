# Create an Artifact Registry repository (GCP's ECR equivalent)
resource "google_artifact_registry_repository" "this" {
  location      = var.region
  repository_id = var.repository_name
  description   = "Docker repository for ${var.repository_name}"
  format        = "DOCKER"
}