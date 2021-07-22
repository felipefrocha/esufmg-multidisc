job "http-echo" {
  datacenters = ["rocha"]	
  group "echo" {
    count = 3
    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "http" {}
    }
    task "echo" {
      driver = "docker"
      config {
        image = "hashicorp/http-echo:latest"
        args = [
          "-listen", ":8080", "-text", "Teste maravilha!"
        ] 
      }
      resources {
        cpu = 100
        memory = 128
      }
    }
  }
}

b0:7b:25:64:ba:b0