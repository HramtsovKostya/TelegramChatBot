# --------------------------------- MAIN ----------------------------------

import config as cnf
from log.logger import DebugLogger

# -------------------------------------------------------------------------

if __name__ == '__main__':
    logger = DebugLogger.get(__name__, file_name=cnf.LOGGING_FILE)
    
    while True:
        logger.debug('This is debug message')
        logger.info('This is info message')
        logger.warning('This is warning message')
        logger.error('This is error message')
        logger.critical('This is fatal error!!!')
        
        if input('\nВведите q для выхода >> ') == 'q':
            break 

# -------------------------------------------------------------------------