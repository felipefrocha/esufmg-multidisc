job "administer" {

  datacenters = ["rocha"]
  
  type = "system"	
  
  group "listener_producer_consumer" {
    count = 1

    network {
      // mbits = 100 # deprecated is no longer considered during the evaluation and scheduling
      port "http" {}
    }

    task "producer" {
      driver = "docker"

      env {
        NAME_FILE = "testeB"
        INTERACTIONS = 1000000
      }
    
      config {
        image = "felipefrocha89/esufmg:multidisc-producer"
        volumes = [
          "/mnt/nfs_clientshare/cidades_info/:/code/cidades_info",
          "/mnt/nfs_clientshare/cidades_raiz/:/code/cidades_raiz:ro",
          "/mnt/nfs_clientshare/saidas/:/code/saidas"
        ]
        args = [
          "-u", "__init__.py"
        ]
        force_pull = true
      }
      
      resources {
        cpu = 256
        memory = 512
      }
    }

    task "consumer" {
      driver = "docker"

      env {
        NAME_FILE = "testeB"
        INTERACTIONS = 1000000
      }
    
      config {
        image = "felipefrocha89/esufmg:multidisc-consumer"
        volumes = [
          "/mnt/nfs_clientshare/saidas/:/code/saidas",
          "/mnt/nfs_clientshare/mapas/:/code/mapas"
        ]
        args = [
          "-u", "__init__.py"
        ]
        force_pull = true
      }
      
      resources {
        cpu = 256
        memory = 512
      }
    }
  }
}