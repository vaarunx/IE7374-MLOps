output "gke_cluster_name" {
  description = "Name of the created GKE cluster"
  value       = module.gke.cluster_name
}

output "artifact_registry_url" {
  description = "Artifact Registry repository URL"
  value       = module.artifact_registry.repository_url
}

output "image_url" {
  description = "Full Docker image URL"
  value       = "${module.artifact_registry.repository_url}/albums-api:latest"
}

output "next_step" {
  description = "Command to deploy your app"
  value       = "Run: kubectl apply -f deployment.yaml"
}