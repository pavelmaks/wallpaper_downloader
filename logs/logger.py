import logging
import os
from logging.handlers import RotatingFileHandler

log_file = 'logs/wallpaper_logs.log'

if not os.path.exists(log_file):
    with open(log_file, 'w'):
        pass

logger = logging.getLogger('wallpaper_application')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler(log_file, maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)
