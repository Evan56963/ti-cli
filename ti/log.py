import logging

logger = logging.getLogger("ti")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger.addHandler(stream_handler)


# file_handler = logging.FileHandler("ti.log", mode='a')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )

# logger.addHandler(file_handler)

# print(logging.Logger.manager.loggerDict.keys())