import os
import logging
from watchdog.events import FileSystemEventHandler
import nomad

###
# Configure logs
###
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
###
# END - Configure logs
###


def create_job(name: str, file_name: str)-> str :
  job =  {
    "Job": {
      "ID": name,
      "Region": "minasgerais",
      "Name": name,
      "Type": "batch",
      "Priority": 50,
      "AllAtOnce": True,
      "Datacenters": [
        "rocha"
      ],
      "TaskGroups": [
        {
          "Name": "processes",
          "Count": 1,
          "RestartPolicy": {
            "Attempts": 0,
            "Interval": 86400000000000,
            "Delay": 15000000000,
            "Mode": "fail"
          },
          "Tasks": [
            {
              "Name": "process",
              "Driver": "docker",
              "User": "",
              "Config": {
                "image": "felipefrocha89/esufmg:multidisc-analyzis",
                "image_pull_timeout": "10m",
                "cpu_hard_limit": True, 
                "ports": [
                  "http"
                ],
                "volumes": [
                  "/mnt/nfs_clientshare/cidades_info:/code/cidades_info",
                  "/mnt/nfs_clientshare/cidades_raiz:/code/cidades_raiz",
                  "/mnt/nfs_clientshare/saidas:/code/saidas"
                ],
                "args": [
                  "-u",
                  "__init__.py",
                  "--file",
                  file_name
                ],
                "force_pull": True
              },
              "Env": {
                "INTERACTIONS": "1000000",
                "NAME_FILE": "testeB"
              },
              "Resources": {
                "CPU": 1024,
                "Cores": 0,
                "MemoryMB": 256,
                "MemoryMaxMB": 512,
                "DiskMB": 0,
                "IOPS": 0,
                "Networks": None,
                "Devices": None
              },
              "RestartPolicy": {
                "Attempts": 0,
                "Interval": 86400000000000,
                "Delay": 15000000000,
                "Mode": "fail"
              },
              "DispatchPayload": None,
              "Lifecycle": None,
              "Meta": None,
              "KillTimeout": 5000000000,
              "LogConfig": {
                "MaxFiles": 10,
                "MaxFileSizeMB": 10
              }
            }
          ],
          "EphemeralDisk": {
            "Sticky": False,
            "SizeMB": 300,
            "Migrate": False
          },

          "Networks": [
            {
              "MBits": 0,
              "DNS": None,
              "DynamicPorts": [
                {
                  "Label": "http",
                  "Value": 0,
                  "To": 0,
                  "HostNetwork": "default"
                }
              ]
            }
          ],
          "Volumes": None

        }
      ]
    }
  }

  nomad_server = nomad.Nomad(host='192.168.15.71')
  response = nomad_server.job.register_job( name, job)
  return response


def delete_job(name: str) -> str :
  nomad_server = nomad.Nomad(host='192.168.15.71')
  response = nomad_server.job.deregister_job(name)
  return response

class MonitorFolder(FileSystemEventHandler):
    FILE_SIZE=100000
    
    def on_created(self, event):
        self.checkFolderSize(event.src_path, event)
   
    def on_modified(self, event):
        self.checkFolderSize(event.src_path, event)
    
                  
    def checkFolderSize(self, src_path, event):
        if os.path.isfile(event.src_path) and event.src_path.endswith(".csv"):
            file_name = event.src_path.split("/")[-1:][0]
            try:
                name = file_name.split(".")[0].replace(" ", "_")
                log.info(f'Deleting previous Job: {name}')
                delete_job(name)
                log.info(f'Job deleted: {name}')

                log.info(f'Creating job {name} with {event.event_type}')
                result = create_job(name, file_name)
                log.info(f'Job Created: {result}')
            except Exception as ex:
                log.error(ex)
        else:
            log.info(f'Ignoring file: {event.src_path}, {event.event_type}')
      