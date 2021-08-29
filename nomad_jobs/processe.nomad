job "distprocess" {

  datacenters = ["rocha"]
  
  type = "batch"	
  
  group "processes" {
    count = 1

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
          "/mnt/nfs_clientshare/docker/:/code"
        ]
        args = []
          "-u", "__init__.py"
        ]
      }
      
      resources {
        cpu = 256
        memory = 512
      }
    }
  }
}