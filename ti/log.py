import logging
from typing import override
from ti.utils.styles import Color, stylize, BgColor, Style

class ColoredFormatter(logging.Formatter):
    """Customized logging formatter with colors based on log level."""
    
    LEVEL_COLOR_MAP: dict[int, Color | BgColor | Style] = {
        logging.DEBUG: Color.BRIGHT_WHITE + BgColor.BRIGHT_BLUE,
        logging.INFO: Color.BRIGHT_WHITE + BgColor.BRIGHT_GREEN,
        logging.WARNING: Color.BRIGHT_WHITE + BgColor.YELLOW,
        logging.ERROR: Color.BRIGHT_WHITE + BgColor.BRIGHT_RED,
        logging.CRITICAL: Color.BRIGHT_WHITE + BgColor.BRIGHT_MAGENTA,
    }

    @override
    def formatTime(self, record: logging.LogRecord, datefmt=None) -> str:
          asctime = super().formatTime(record, datefmt)
         
          return stylize(asctime, Color.GREEN)
    
    @override
    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLOR_MAP.get(record.levelno, Color.WHITE)
        record.name = stylize(record.name, Color.CYAN)
        record.levelname = stylize(record.levelname, color)
        record.msg = stylize(record.msg, Color.WHITE)
        
        return super().format(record)


logger = logging.getLogger("ti")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(
    ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

yf_logger = logging.getLogger("yfinance")
yf_logger.setLevel(logging.WARNING)
yf_stream_handler = logging.StreamHandler()
yf_stream_handler.setLevel(logging.WARNING)
yf_stream_handler.setFormatter(
    ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger.addHandler(stream_handler)
yf_logger.addHandler(yf_stream_handler)


# file_handler = logging.FileHandler("ti.log", mode='a')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )

# logger.addHandler(file_handler)
# print(logging.Logger.manager.loggerDict.keys())