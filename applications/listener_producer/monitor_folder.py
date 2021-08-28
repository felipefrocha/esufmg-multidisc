import os
import logging
from watchdog.events import FileSystemEventHandler
import nomad


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
                "ports": [
                  "http"
                ],
                "volumes": [
                  "/mnt/nfs_clientshare/cidades_info:/code/cidades_info",
                  "/mnt/nfs_clientshare/cidade_raiz:/code/cidades_raiz",
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
                "CPU": 2000,
                "Cores": 0,
                "MemoryMB": 720,
                "MemoryMaxMB": 0,
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

class MonitorFolder(FileSystemEventHandler):
    FILE_SIZE=100000
    
    def on_created(self, event):
        self.checkFolderSize(event.src_path, event)
   
    def on_modified(self, event):
        self.checkFolderSize(event.src_path, event)
    
                  
    def checkFolderSize(self, src_path, event):
        if os.path.isfile(event.src_path) and event.src_path.endswith(".csv"):
            file_name = event.src_path.split("/")[-1:][0]
            log.info(f'Creating job {file_name} with {event.event_type}')
            try:
              create_job(file_name.split(".")[0].replace(" ", "_"), file_name)
            except ex:
              log.error(ex)
        else:
            log.info(f'Ignoring file: {event.src_path}, {event.event_type}')
      