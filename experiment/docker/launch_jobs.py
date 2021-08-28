import os
import sys
import logging

import nomad

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

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

def create_job(name: str)-> str :
  job =  {
    "Job": {
      "ID": "name",
      "Region": "minasgerais",
      "Name": "name",
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
                "image": "felipefrocha89/esufmg:multidisc",
                "ports": [
                  "http"
                ],
                "volumes": [
                  "/mnt/nfs_clientshare/cidade_raiz:/code/files"
                ],
                "args": [
                  "-u",
                  "__init__.py"
                ]
              },
              "Env": {
                "INTERACTIONS": "1000000",
                "NAME_FILE": "testeB"
              },
              "Resources": {
                "CPU": 256,
                "Cores": 0,
                "MemoryMB": 512,
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


def main():
  pass


def on_created(event):
    log.info(f"hey, {event.src_path} has been created!")
    print("teste")
    # crete_job(event.src_path)

def on_modified(event):
    log.info(f"hey buddy, {event.src_path} has been modified")


def create_event_handler():
    log.info('EVENT HANDLER - Creating a new Event Handler for CSV files')
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True

    log.info('EVENT HANDLER - Configuring new Event Handler')
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified

    return event_handler


def create_observer(event_handler):
    log.info('OBSERVER - Geting File path to Observe')
    path = f'{os.path.abspath(os.getcwd())}/files'
    go_recursively = True
    observer = Observer()

    log.info(f'OBSERVER - Configure new Observer on {path}')
    observer.schedule(event_handler, path, recursive=go_recursively)
    
    return observer


def create_pipe():
    event_handler = create_event_handler()
    if event_handler is None:
        log.error('It was not possible to create a new Event Handler')
        exit(1)

    observer = create_observer(event_handler)
    if observer is None:
        log.error('It was not possible to create a new Observer')
        exit(1)

    observer.start()
    log.info(f'OBSERVER - Now listening...')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    log.info('Initializing Listener')
    try:
        create_pipe()
    except KeyboardInterrupt:
        log.error('Get out of here!')
    log.info('Finishing Listening to folder')
    exit(0)