import os
import one_config
from one_config.config import ConfigError

def config():
    try:
        return one_config.get_config()
    except ConfigError:
        # one_config.build_config() can be called only once, so it will fail if we call multiple times.
        loadConfig()
        return one_config.get_config()

def loadConfig():
    """
    If env var WEBMON_CONFIG_FILE is set, it will read the file from there, otherwise default to config.yaml.
    """
    one_config.build_config().from_yaml(os.getenv('WEBMON_CONFIG_FILE', 'config.yaml'))


