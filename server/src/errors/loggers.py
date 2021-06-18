import logging
import graypy

aam_logger = logging.getLogger('aam_logger')
aam_logger.setLevel(logging.DEBUG)
handler = graypy.GELFUDPHandler('localhost', 12201)
aam_logger.addHandler(handler)
