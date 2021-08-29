job "grafana" {
  datacenters = ["rocha"]

  type = "service"

  constraint {
    attribute = "${attr.kernel.name}"
    value = "linux"
  }

  update {
    stagger = "30s"
    max_parallel = 1
  }

  group "grafana" {

    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "http" {}
    }

    restart {
      attempts = 10
      interval = "5m"
      delay = "10s"
      mode = "delay"
    }

    task "grafana" {
      driver = "docker"
      config {
        image = "grafana/grafana:latest"
        ports = ["http"]
      }

      env {
        GF_LOG_LEVEL = "DEBUG"
        GF_LOG_MODE = "console"
        GF_SERVER_HTTP_PORT = "${NOMAD_PORT_http}"
        GF_INSTALL_PLUGINS = "grafana-clock-panel,grafana-simple-json-datasource"
      }

      resources {
        cpu    = 512
        memory = 1000
      }
    }

    service {
      tags = ["urlprefix-/grafana strip=/grafana"]
      name = "grafana" 
      port = "http"
      check {
        name     = "Grafana HTTP"
        type     = "http"
        path     = "/api/health"
        interval = "5s"
        timeout  = "2s"
        check_restart {
          limit = 2
          grace = "160s"
          ignore_warnings = false
        }
      }
    }
  }
}
