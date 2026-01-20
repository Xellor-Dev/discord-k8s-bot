# terraform/main.tf

# 1. Создаем саму виртуальную сеть (VPC)
resource "google_compute_network" "vpc" {
  name                    = "discord-bot-vpc"
  auto_create_subnetworks = false # ВАЖНО: Отключаем "автомагию". Мы создадим подсети сами.
}

# 2. Создаем подсеть (Subnet) в нашем регионе
# Именно в этой подсети будут жить твои узлы Kubernetes
resource "google_compute_subnetwork" "subnet" {
  name          = "discord-bot-subnet"
  ip_cidr_range = "10.0.0.0/24" # Диапазон IP: от 10.0.0.0 до 10.0.0.255
  region        = "us-central1" # Айова (дешево)
  network       = google_compute_network.vpc.id
}