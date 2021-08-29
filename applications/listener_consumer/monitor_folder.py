import os
import logging
from watchdog.events import FileSystemEventHandler
from consolidar_cidades import consolidar_cidades

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
            try:
                log.info(f'Consolidate City {file_name} with {event.event_type}')
                consolidar_cidades(file_name)
            except Exception as ex:
              log.error(ex)
        else:
            log.info(f'Ignoring file: {event.src_path}, {event.event_type}')
      
      