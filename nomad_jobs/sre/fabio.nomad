job "fabio" {
  datacenters = ["rocha"]
  type = "system"

  group "fabio" {
    network {
      # mbits = 20
      port "lb" {
        static = 9999
      }
      port "ui" {
        static = 9998
      }
    }
    task "fabio" {
      driver = "docker"
      config {
        image = "fabiolb/fabio"
        network_mode = "host"
      }

      resources {
        cpu    = 100
        memory = 64
      }
    }
  }
}
