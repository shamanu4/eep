from .base import *


class LocalSettingsException(Exception):
    pass


try:
    from .local import *
except ImportError as exc:
    raise LocalSettingsException('%s (did you rename settings/local-dist.py?)' % exc.args[0])