import importlib

from .config_metaclass import ConfigMetaClass
from .system_config import SystemConfig
from .default_components import Components


def init(exp: str):
    exp = exp.replace('/', '.')
    importlib.import_module(f'configs.{exp}')
    SystemConfig.exp = exp
    SystemConfig.exp_path = exp.replace('.', '/')
