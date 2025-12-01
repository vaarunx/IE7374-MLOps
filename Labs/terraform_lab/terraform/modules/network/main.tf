# Create VPC network
resource "google_compute_network" "this" {
  name                    = "${var.service_name}-vpc"
  auto_create_subnetworks = false
}

# Create subnet
resource "google_compute_subnetwork" "this" {
  name          = "${var.service_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.this.id

  # Enable private Google access for pulling images from Artifact Registry
  private_ip_google_access = true
}

# Firewall rule to allow HTTP traffic
resource "google_compute_firewall" "allow_http" {
  name    = "${var.service_name}-allow-http"
  network = google_compute_network.this.name

  allow {
    protocol = "tcp"
    ports    = ["80", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = [var.service_name]
}

# Firewall rule to allow health checks
resource "google_compute_firewall" "allow_health_check" {
  name    = "${var.service_name}-allow-health-check"
  network = google_compute_network.this.name

  allow {
    protocol = "tcp"
  }

  # GCP health check IP ranges
  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
  target_tags   = [var.service_name]
}