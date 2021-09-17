job "cadvisor" {
  datacenters = ["rocha"]

  type = "system"

  group "cadvisor" {

    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "cadvisor" {
        static = 8080
      }
    }

    task "cadvisor" {
      driver = "docker"

      config {
        image = "google/cadvisor:latest"

        ports = ["cadvisor"]
      }

      resources {
        cpu = 100
        memory = 128
      }
    }

    service {
      tags = ["urlprefix-/cadvisor strip=/cadvisor"]
      name = "cadvisor" 
      port = "cadvisor"

      check {
        type = "http"
        path = "/"
        interval = "10s"
        timeout = "2s"
      }
    }
  }
}
