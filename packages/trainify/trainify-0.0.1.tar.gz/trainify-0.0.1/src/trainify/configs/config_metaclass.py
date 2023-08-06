from typing import Tuple
import logging


class ConfigMetaClass(type):
    def __new__(mcs, name: str, bases: Tuple[type, ...], attrs_dict: dict) -> type:
        if not bases:
            config_class = super().__new__(mcs, name, bases, attrs_dict)
            config_class.__initialized__ = False
            return config_class
        for base in bases:
            assert isinstance(base, ConfigMetaClass), f'{name} inherited from non-config class {base}'
            assert not base.__initialized__, f'{name} trying to override already initialized {base}'
        unused_keys = []
        for key, value in attrs_dict.items():
            if not key.startswith('_'):
                is_unused = True
                for base in bases:
                    if hasattr(base, key):
                        setattr(base, key, value)
                        is_unused = False
                if is_unused:
                    unused_keys.append(key)
        if unused_keys:
            logging.warning(f'Attributes {unused_keys} of {name} were not used, rename to _[name] to suppress warning')
        for base in bases:
            if hasattr(base, 'init'):
                base.init()
        return super().__new__(mcs, name, bases, attrs_dict)
