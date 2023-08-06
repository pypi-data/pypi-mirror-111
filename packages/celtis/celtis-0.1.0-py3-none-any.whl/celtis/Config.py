from appdirs import AppDirs
from glob import glob
import yaml, pathlib, os

__appname__ = 'celtis'
__author__ = '0xcrypto'
__version__ = '0.1.0'

def build_dir(dirtype:str, path=''):
    """Builds os independent file locations to default storage of rules and configuration"""
    return getattr(AppDirs(__appname__, __author__, version=__version__), dirtype) + '/' + path.strip('/')  

def config(key):
    """Gives value for a configuration key."""
    for x in range(3):
        try:
            with open(build_dir('user_data_dir', 'config.yml'), "r") as config:
                configuration = yaml.load(config, Loader=yaml.FullLoader)
            break
        except FileNotFoundError:
            logger.debug('No configuration found, creating default configuration.')
            pathlib.Path(build_dir('user_data_dir')).mkdir(parents=True, exist_ok=True)
            with open(build_dir('user_data_dir', 'config.yml'), "w") as defaultConfig:
                defaultConfigData = {
                    "rules_dir": build_dir('user_data_dir', 'rules')
                }
                yaml.dump(defaultConfigData, defaultConfig, Dumper=yaml.Dumper)
    return configuration[key]

def get_rules(rules_dir=None):
    """Returns rules from the rules directory"""
    if(not rules_dir):
        rules_dir = config('rules_dir')
    
    return [os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(rules_dir, "*.py"))]
