from functools import lru_cache

import yaml


@lru_cache()
def get_config():
    """
    :return: Config Dictionary
    """
    with open("CONFIG.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
        config_openai = config["openai"]
        config_db = config["database"]
        config_env = config["environment"]

        return config_env, config_openai, config_db
