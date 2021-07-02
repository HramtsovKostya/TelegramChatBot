# ----------------------------- MAIN --------------------------------------

import time
from log.logger import DebugLogger

# -------------------------------------------------------------------------

def start_logger():
    logger = DebugLogger.get(__name__)

    for _ in range(10):
        logger.debug('This is a debug message')
        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a fatal error!!!')
        time.sleep(1)
   
# -------------------------------------------------------------------------    

if __name__ == '__main__':
    start_logger()
    
# -------------------------------------------------------------------------   
