from celtis.Config import *
from multiprocessing import Pool
from celtis.Logger import logger
import sys, yaml, importlib
from importlib.machinery import SourceFileLoader

def stopscan():
    logger.debug("Exitting...")
    exit()

class Scanner:
    def __init__(self, targets, process:int):
        self.targets = targets
        self._maxprocess_count = process
        sys.path.append(config('rules_dir'))
        sys.path = list(set(sys.path))

    def loop(self):
        """Loop over all the targets to spawn processes"""
        while True:
            targets = self.targets.pluck(self._maxprocess_count)

            with Pool(self._maxprocess_count) as pool:
                pool.map(Scanner.scan, targets)

    def scan(target):
        """Single Target Scanner."""
        logger.debug("Starting scan on target: %s" % target)
        for rule in get_rules():
            logger.debug("Running scan rule: %s" % rule)
            rule = SourceFileLoader(rule).load_module()
            logger.debug(rule)
            # importlib.import_module(rule)

        # 1. detect technology
        # 2. fingerprint more technologies
        # 2. load correct scan rule
