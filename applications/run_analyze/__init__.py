import os
import sys
import argparse
from typing import Callable
# Custom code
from cidades_raiz import *


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


def parse_args():
    parser = argparse.ArgumentParser(
                                    prog="CityProcess",
                                    usage='%(prog)s [options] file',
                                    description='Process city files',
                                    allow_abbrev=False,
                                    epilog='Enjoy the program! :)'
                                    )
    parser.version = '1.0'

    parser.add_argument('--file',
                       action='store',
                       metavar='File',
                       type=str,
                       required=True,
                       help='The file path to be analised')
    
    args = parser.parse_args()
    input_path_to_file = args.file

    if not os.path.isdir('/code/cidades_info/'):
        log.error(f'The folder is not mounted')
        exit(1)
    
    log.info(os.listdir('/code/cidades_info/'))

    if not os.path.isfile(f'/code/cidades_info/{input_path_to_file}'):
        log.error(f'The path specified does not exist {input_path_to_file}')
        exit(1)

    return input_path_to_file
    

def main():
    try:
        file_path = parse_args()
    except Exception as ex:
        log.error('Something is wrong in parser')
        exit(1)
        
    log.info(f"Initialize analyzis {file_path}")

    try:    
        process_city(file_path)
    except Exception as ex:
        log.error(ex)


if __name__ == "__main__":
    log.info('Initializing routines')
    main()
    exit(0)
