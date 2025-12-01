# GKE Autopilot Cluster (closest to ECS Fargate)
resource "google_container_cluster" "this" {
  name     = "${var.service_name}-cluster"
  location = var.region

  # Autopilot mode - fully managed like Fargate
  enable_autopilot = true
  
  # Disable deletion protection for easier cleanup
  deletion_protection = false

  network    = var.network_name
  subnetwork = var.subnetwork_name

  # IP allocation for pods and services
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/16"
    services_ipv4_cidr_block = "/22"
  }

  # Enable logging and monitoring
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }
}