job "distprocess" {
  datacenters = ["rocha"]
  type = "batch"	
  group "processes" {
    count = 3

    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "http" {}
    }

    task "process" {
      driver = "docker"

      env {
        NAME_FILE = "testeB"
        INTERACTIONS = 1000000
      }
    
      config {
        image = "felipefrocha89/testepy:latest"
        ports = ["http"]
        volumes = [
          "/home/vagrant/docker/:/code"
        ]
      }
      
      resources {
        cpu = 256
        memory = 512
      }
    }
  }
}