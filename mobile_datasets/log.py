import logging
import sys

def setup_logging(level=logging.INFO):
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p', level=level)
