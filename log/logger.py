# -------------------------------- LOGGER ---------------------------------

import sys
import logging as log

# -------------------------------------------------------------------------

class DebugLogger(object):
    __LOG_FORMAT = 'TIME: [ %(asctime)s ] - LEVEL: [ %(levelname)-8s ]'
    __LOG_FORMAT += ' - LOCATE: [ %(filename)s / %(funcName)s() / '
    __LOG_FORMAT += 'LINE: %(lineno)d ] - MESSAGE: [ %(message)-25s ]'
    
    #? >>> HELP >>>           Уровни логирования           <<<< HELP <<<<
    #* 1. NOTSET   =  0 - Все сообщения отключены
    #* 2. DEBUG    = 10 - Подробная информация для диагностики проблем
    #* 3. INFO     = 20 - Подтверждение об исправной работе прогрраммы
    #* 4. WARNING  = 30 - Произошла проблема, но код все еще работает (default)
    #* 5. ERROR    = 40 - Ошибка при выполнении какой-либо функции
    #* 6. CRITICAL = 50 - Серьезная ошибка, выполнение кода прервалось
    #? >>> HELP >>>           Уровни логирования           <<<< HELP <<<<
    
    __DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
    
    #? >>> HELP >>>           Форматирование даты           <<<< HELP <<<<
    #* %a — будний день сокращенно (Mon, Tue,…)
    #* %A — будний день полностью (Monday, Tuesday,…)
    #* %w — будний день, как десятичное число (1, 2, 3,…)
    #* %d — день месяца в числах (01, 02, 03,…)
    #* %b — месяцы сокращенно (Jan, Feb,…)
    #* %B — название месяцев полностью (January, February,…)
    #* %m — месяцы в числах (01, 02, 03,…)
    #* %y — года без века (19, 20, 21)
    #* %Y — года с веком (2019, 2020, 2021)
    #* %H — 24 часа в сутки (с 00 до 23)
    #* %I — 12 часов в сутки (с 01 до 12)
    #* %p — AM и PM (00-12 и 12-00)
    #* %M — минуты (от 00 до 59)
    #* %S — секунды (от 00 до 59)
    #* %f — миллисекунды (6 десятичных чисел)
    #? >>> HELP >>>           Форматирование даты           <<<< HELP <<<<
  
 # ------------------------------------------------------------------------- 
    
    @staticmethod
    def get(name: str, file_name: str):
        fmt = DebugLogger.__formatter()
        
        file_hdl = DebugLogger.__file_handler(fmt, file_name)
        str_hdl = DebugLogger.__str_handler(fmt)
        
        logger = log.getLogger(name)
        logger.setLevel(log.DEBUG)        

        logger.addHandler(file_hdl)
        logger.addHandler(str_hdl) 
        return logger

    @staticmethod
    def __formatter():
        return log.Formatter(
            fmt=DebugLogger.__LOG_FORMAT,
            datefmt=DebugLogger.__DATE_FORMAT
        )
    
    @staticmethod
    def __file_handler(fmt: log.Formatter, file_name: str):
        hdl = log.FileHandler(file_name)
        hdl.setLevel(log.DEBUG)
        hdl.setFormatter(fmt)
        return hdl

    @staticmethod
    def __str_handler(fmt: log.Formatter, stream=sys.stderr):
        hdl = log.StreamHandler(stream)
        hdl.setLevel(log.WARNING)
        hdl.setFormatter(fmt)
        return hdl

# -------------------------------------------------------------------------