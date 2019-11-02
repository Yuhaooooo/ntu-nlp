from pathlib import Path
from typing import Union

import yaml

# project directory
BASE_DIR = Path(__file__).absolute().parent / '..'

DATA_DIR = str(BASE_DIR / 'data')
OUTPUT_DIR = str(BASE_DIR / 'output')


def _parse_config() -> Union[dict, list, None]:
    with open(BASE_DIR / 'configs/config.yaml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


configs = _parse_config()

__all__ = ['BASE_DIR', 'DATA_DIR', 'OUTPUT_DIR', 'configs']
