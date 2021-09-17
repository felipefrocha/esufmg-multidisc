import os
import sys
import time
import logging
from monitor_folder import MonitorFolder
from watchdog.observers import Observer


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



def create_observer(event_handler):
    log.info('OBSERVER - Geting File path to Observe')
    path = f'{os.path.abspath(os.getcwd())}/cidades_info'
    go_recursively = True
    observer = Observer()

    log.info(f'OBSERVER - Configure new Observer on {path}')
    observer.schedule(event_handler, path, recursive=go_recursively)
    
    return observer

def create_pipe():
    event_handler = MonitorFolder()
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
    log.info('Initializing Producere Listener')
    try:
        create_pipe()
    except KeyboardInterrupt:
        log.error('Get out of here!')
    log.info('Finishing Listening to folder')
    exit(0)