import os


def read_config_file(section, key):
    from configparser import ConfigParser
    from pathlib import Path
    from pathlib import PurePosixPath

    config_path = PurePosixPath.joinpath(Path(__file__).parent.parent).joinpath('config.ini')

    config = ConfigParser()
    config.read(config_path)

    value = config.get(section, key)

    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False

    return value


def read_config_from_current_env(key):
    section = os.getenv('env').lower()
    return read_config_file(section, key)


def read_config_file_with_validation(section, key):
    try:
        return read_config_file(section, key)
    except:
        return None
