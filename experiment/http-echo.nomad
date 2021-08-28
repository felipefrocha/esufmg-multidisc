job "http-echo" {
  datacenters = ["rocha"]	
  group "echos" {
    count = 120
    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "http" {}
    }
    task "echo" {
      driver = "docker"
      config {
        image = "hashicorp/http-echo:latest"
        args = [
          "-listen", ":${NOMAD_PORT_http}",
          "-text", "Essa é a task ${NOMAD_TASK_NAME} da Giropops App que está sendo executado no IP ${NOMAD_IP_http} rodando na porta ${NOMAD_PORT_http}.",  
        ]
        ports = ["http"]
      }
      resources {
        cpu = 100
        memory = 128
      }
    }
  }
}