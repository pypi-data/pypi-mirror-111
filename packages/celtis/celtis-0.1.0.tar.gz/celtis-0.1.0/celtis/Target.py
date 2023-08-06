from celtis.Logger import logger
from celtis.Scanner import stopscan

class Target:
    def __init__(self, resource):
        """Wrapper for the target resource"""
        self.targets = enumerate(resource)
        self._current_value = (None, None)

    def next(self):
        """Gives next target"""
        try:
            self._current_value = next(self.targets)
        except StopIteration:
            logger.debug("Scanned all targets.")
            stopscan()

        return self.current()

    def current(self):
        """Gives current Target"""
        if(None == self._current_value[0]):
            return self.next()
        return str(self._current_value[1]).strip()

    def index(self):
        """Gives index of current target in provided resource"""
        return int(self._current_value[0])

    def pluck(self, items:int):
        """Plucks next n items from the resource"""
        return [self.current() for nextenum in ([self.next] * items) if nextenum()]

    def current_raw(self):
        """Returns tuple having index and raw value."""
        return self._current_value