import asyncio
from socket import gaierror
from typing import Tuple

from aiohttp import ClientError, ClientSession
from awesomeversion import AwesomeVersion

from pyopversion.exceptions import OpVersionFetchException, OpVersionParseException

from .base import OpVersionBase
from .consts import (
    DEFAULT_BOARD,
    DEFAULT_TIMEOUT,
    LOGGER,
    OpVersionChannel,
    OpVersionSource,
)
from .container import OpVersionContainer
from .opio import OpVersionOpio
from .local import OpVersionLocal
from .pypi import OpVersionPypi
from .supervisor import OpVersionSupervisor


class OpVersion(OpVersionBase):
    def __init__(
        self,
        session: ClientSession = None,
        source: OpVersionSource = OpVersionSource.DEFAULT,
        channel: OpVersionChannel = OpVersionChannel.DEFAULT,
        board: str = DEFAULT_BOARD,
        image: str = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.board = board
        self.channel = channel
        self.session = session
        self.source = source
        self.image = image
        self.timeout = timeout

        handler_args = {
            "board": board,
            "channel": channel,
            "session": session,
            "image": image,
            "source": source,
            "timeout": timeout,
        }
        if self.source == OpVersionSource.CONTAINER:
            self._handler = OpVersionContainer(**handler_args)
        elif self.source == OpVersionSource.PYPI:
            self._handler = OpVersionPypi(**handler_args)
        elif self.source == OpVersionSource.SUPERVISOR:
            self._handler = OpVersionSupervisor(**handler_args)
        elif self.source == OpVersionSource.OPIO:
            self._handler = OpVersionOpio(**handler_args)
        else:
            self._handler = OpVersionLocal(**handler_args)

    @property
    def version(self) -> AwesomeVersion:
        """Return the version."""
        return self._handler.version

    @property
    def version_data(self) -> dict:
        """Return extended version data for supported sources."""
        return self._handler.version_data

    async def get_version(self) -> Tuple[AwesomeVersion, dict]:
        try:
            await self._handler.fetch()

        except asyncio.TimeoutError as exception:
            raise OpVersionFetchException(
                f"Timeout of {self.timeout} seconds was reached while fetching version for {self.source}"
            ) from exception

        except (ClientError, gaierror, ImportError, ModuleNotFoundError) as exception:
            raise OpVersionFetchException(
                f"Error fetching version information from {self.source} {exception}"
            ) from exception

        try:
            self._handler.parse()

        except (KeyError, TypeError) as exception:
            raise OpVersionParseException(
                f"Error parsing version information for {self.source} - {exception}"
            ) from exception

        LOGGER.debug("Version: %s", self.version)
        LOGGER.debug("Version data: %s", self.version_data)
        return self.version, self.version_data
