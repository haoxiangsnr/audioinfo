from importlib import metadata

__version__ = metadata.metadata(__package__)["version"]
