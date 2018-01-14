import logging
import os

logsdir = "logs"

logger = logging.getLogger("activecampaign3")
os.makedirs(logsdir, exist_ok=True)
logfilepath = os.path.join(logsdir, "debug.log")
h = logging.FileHandler(logfilepath)
h.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)
logger.setLevel(logging.DEBUG)
