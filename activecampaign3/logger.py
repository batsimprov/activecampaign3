from activecampaign3.config import CONFIG
import logging
import os

logsdir = CONFIG['logs']['dir']
log_level = getattr(logging, CONFIG['logs']['level'].upper())

logger = logging.getLogger("activecampaign3")
os.makedirs(logsdir, exist_ok=True)
logfilepath = os.path.join(logsdir, CONFIG['logs']['file'])
h = logging.FileHandler(logfilepath)
h.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)
logger.setLevel(log_level)
