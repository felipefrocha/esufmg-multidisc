datacenter = "rocha"

data_dir = "/opt/consul"

ui_config {
  enabled = true
}

server = true

bind_addr = "0.0.0.0" # Listen on all IPv4

advertise_addr = "192.168.15.55"

bootstrap_expect=1