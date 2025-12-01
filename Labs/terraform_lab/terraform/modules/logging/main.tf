# Cloud Logging sink for GKE container logs
# Note: GKE automatically sends logs to Cloud Logging, but we can create a log sink for filtering

resource "google_logging_project_sink" "this" {
  name        = "${var.service_name}-logs"
  destination = "logging.googleapis.com/projects/${data.google_project.current.project_id}/logs/${var.service_name}"

  # Filter to only include logs from this service
  filter = "resource.type=k8s_container AND resource.labels.namespace_name=${var.service_name}"

  unique_writer_identity = true
}

data "google_project" "current" {}