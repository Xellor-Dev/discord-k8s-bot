terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "sharp-oxygen-478014-k9"
  region  = "us-central1"
  zone    = "us-central1-a"
}