import os
import pathlib
import yaml


CONFIG_DIR = pathlib.Path(os.environ['CONFIG_DIR'])
app_config_path = CONFIG_DIR / 'app.yaml'
mongo_config_path = CONFIG_DIR / 'mongo.yaml'
logging_config_path = CONFIG_DIR / 'logging.yaml'
services_config_path = CONFIG_DIR / 'services.yaml'
storage_config_path = CONFIG_DIR / 'storage.yaml'


def get_config(path):
    with open(path) as f:
        conf = yaml.safe_load(f)
    return conf


app_config = get_config(app_config_path)
logging_config = get_config(logging_config_path)
services_config = get_config(services_config_path)
mongo_config = get_config(mongo_config_path)
storage_config = get_config(storage_config_path)


__all__ = [
    'get_config',
    'app_config',
    'logging_config',
    'services_config',
    'mongo_config',
    'storage_config',
]
