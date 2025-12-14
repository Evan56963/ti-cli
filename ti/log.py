import logging
from typing import override
from ti.utils.colors import Colors, stylize

class ColoredFormatter(logging.Formatter):

    LEVEL_COLOR_MAP = {
        logging.DEBUG: Colors.BRIGHT_WHITE,
        logging.INFO: Colors.BRIGHT_GREEN,
        logging.WARNING: Colors.BRIGHT_YELLOW,
        logging.ERROR: Colors.BRIGHT_RED,
        logging.CRITICAL: Colors.BRIGHT_MAGENTA,
    }

    @override
    def formatTime(self, record: logging.LogRecord, datefmt=None) -> str:
          asctime = super().formatTime(record, datefmt)
         
          return stylize(asctime, Colors.CYAN)
    
    @override
    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLOR_MAP.get(record.levelno, Colors.WHITE)
        record.name = stylize(record.name, Colors.CYAN)
        record.levelname = stylize(record.levelname, color)
        record.msg = stylize(record.msg, Colors.WHITE)
        
        return super().format(record)


logger = logging.getLogger("ti")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(
    ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger.addHandler(stream_handler)


# file_handler = logging.FileHandler("ti.log", mode='a')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )

# logger.addHandler(file_handler)
# print(logging.Logger.manager.loggerDict.keys())