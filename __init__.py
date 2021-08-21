from typing import Callable

from cidades_raiz import *
from consolidar_cidades import *

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
    
if __name__ == "__main__":
    log.info('Initializing routines')

    for i in range(9):
        cidades_raiz(i+1)
    
    consolidar_cidades()
    exit(0)
