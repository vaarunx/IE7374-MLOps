output "network_name" {
  description = "VPC network name"
  value       = google_compute_network.this.name
}

output "subnetwork_name" {
  description = "Subnet name"
  value       = google_compute_subnetwork.this.name
}

output "network_id" {
  description = "VPC network ID"
  value       = google_compute_network.this.id
}