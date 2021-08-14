job "consul" {
  datacenters = ["rocha"]
  group "consul" {
    count = 1
    task "consul" {
      driver = "exec"
      config {
        command = "consul"
        args = [ "agent", "-dev" ]
      }
      artifact {
        source = "
      }
    }
  }
}