"""OpVersionLocal class."""
from .base import OpVersionBase


class OpVersionLocal(OpVersionBase):
    """OpVersionLocal class."""

    async def fetch(self):
        """Logic to fetch new version data."""
        from openpeerpower.const import __version__ as localversion

        self._data = localversion

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data
