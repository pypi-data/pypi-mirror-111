"""Exceptions for pyopversion."""


class OpVersionException(Exception):
    """Base pyopversion exception."""


class OpVersionInputException(OpVersionException):
    """Raised when missing required input."""


class OpVersionFetchException(OpVersionException):
    """Raised there are issues fetching information."""


class OpVersionParseException(OpVersionException):
    """Raised there are issues parsing information."""
