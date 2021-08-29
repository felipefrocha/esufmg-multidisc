job "monitoring" {
  datacenters = ["rocha"]
  type        = "service"

  group "prometheus" {
    count = 1

    restart {
      attempts = 2
      interval = "30m"
      delay    = "15s"
      mode     = "fail"
    }

    network {
      # mbits = 10
      port  "prometheus_ui"{
        to = 9090
      }
    }

    ephemeral_disk {
      size = 300
    }

    task "prometheus" {
      template {
        change_mode = "noop"
        destination = "local/webserver_alert.yml"
        data = <<EOH
---
groups:
- name: prometheus_alerts
  rules:
  - alert: Webserver down
    expr: absent(up{job="webserver"})
    for: 10s
    labels:
      severity: critical
    annotations:
      description: "Our webserver is down."
EOH
      }

      template {
        change_mode = "noop"
        destination = "local/prometheus.yml"
        data = <<EOH
---
global:
  scrape_interval:     5s
  evaluation_interval: 5s

alerting:
  alertmanagers:
  - consul_sd_configs:
    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
      services: ['alertmanager']

rule_files:
  - "webserver_alert.yml"

scrape_configs:

  - job_name: 'alertmanager'

    consul_sd_configs:
    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
      services: ['alertmanager']

  - job_name: 'nomad_metrics'

    consul_sd_configs:
    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
      services: ['nomad-client', 'nomad']

    relabel_configs:
    - source_labels: ['__meta_consul_tags']
      regex: '(.*)http(.*)'
      action: keep

    scrape_interval: 5s
    metrics_path: /v1/metrics
    params:
      format: ['prometheus']

  - job_name: 'webserver'

    consul_sd_configs:
    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
      services: ['webserver']
    metrics_path: /metrics

#  - job_name: mngt_consul_service
#
#    consul_sd_configs:
#    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
#      services: ['consul']
#    
#    relabel_configs:
#    - action: keep
#      regex: management-service
#      source_labels:
#      - __meta_consul_service

  - job_name: 'cadvisor'
    consul_sd_configs:
    - server: '{{ env "NOMAD_IP_prometheus_ui" }}:8500'
      services: ['cadvisor']
    metrics_path: /metrics

EOH
      }
      driver = "docker"
      config {
        image = "prom/prometheus:latest"
        volumes = [
          "local/webserver_alert.yml:/etc/prometheus/webserver_alert.yml",
          "local/prometheus.yml:/etc/prometheus/prometheus.yml"
        ]

        ports = ["prometheus_ui"]
      }

      service {
        name = "prometheus"
        tags = ["urlprefix-/"]
        port = "prometheus_ui"

        check {
          name     = "prometheus_ui port alive"
          type     = "http"
          path     = "/-/healthy"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }

  group "alerting" {
    count = 1
    restart {
      attempts = 2
      interval = "30m"
      delay = "15s"
      mode = "fail"
    }
    ephemeral_disk {
      size = 300
    }

    network {
      # mbits = 10
      port "alertmanager_ui" {
        to = 9093
      }
    }

    task "alertmanager" {
      driver = "docker"
      config {
        image = "prom/alertmanager:latest"
        ports = ["alertmanager_ui"]
        
      }

      service {
        name = "alertmanager"
        tags = ["urlprefix-/alertmanager strip=/alertmanager"]
        port = "alertmanager_ui"
        check {
          name     = "alertmanager_ui port alive"
          type     = "http"
          path     = "/-/healthy"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }

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

      template {
        change_mode = "noop"
        destination = "local/grafana.ini"
        data = <<EOH
[server]
root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana/
serve_from_sub_path = true
EOH
      }
      driver = "docker"
      config {
        image = "grafana/grafana:latest"
        ports = ["http"]
        volumes = [
          "local/grafana.ini:/etc/grafana/grafana.ini"
        ]
      }

      env {
        GF_LOG_LEVEL = "DEBUG"
        GF_LOG_MODE = "console"
        GF_SERVER_HTTP_PORT = "${NOMAD_PORT_http}"
        GF_INSTALL_PLUGINS = "grafana-clock-panel,grafana-simple-json-datasource,natel-discrete-panel,grafana-piechart-panel"
        GF_PATHS_CONFIG = "/etc/grafana/grafana.ini"
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
