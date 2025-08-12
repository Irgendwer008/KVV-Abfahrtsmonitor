import logging
import sys

logger = logging.getLogger("KVV-Abfahrtsmonitor")
logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s:%(module)s:%(lineno)s:%(message)s", filename="KVV-Abfahrtsmonitor.log", filemode="w", encoding="utf-8", level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))