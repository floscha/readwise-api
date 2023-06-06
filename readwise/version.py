from importlib import metadata

__version__ = metadata.version("readwise-api")

del metadata  # avoid polluting the results of dir(__package__)