# terraform/gke.tf

# 1. Сначала удаляем дефолтный Node Pool (рекомендация Google)
# Мы создадим свой, настроенный кастомно.
resource "google_container_cluster" "primary" {
  name     = "discord-bot-cluster"
  location = "us-central1-a" # Зональный кластер (дешевле регионального)
  
  # Привязываем к нашей сети, которую создали минуту назад
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Удаляем дефолтный пул сразу после создания мастера
  remove_default_node_pool = true
  initial_node_count       = 1
  
  # Отключаем удаление при ошибке (чтобы видеть логи)
  deletion_protection = false 
}

# 2. Создаем наш Node Pool (рабочие лошадки)
resource "google_container_node_pool" "primary_nodes" {
  name       = "discord-bot-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.primary.name
  
  node_count = 1 # Одна нода. Для бота хватит за глаза.

  node_config {
    # e2-medium (2 vCPU, 4GB RAM) - оптимальный баланс
    machine_type = "e2-medium"

    # !!! ЭКОНОМИЯ !!!
    # Используем Spot VM (они дешевые, но Google может их перезагрузить)
    spot = true 

    # OAuth права для нод (чтобы они могли качать образы)
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}