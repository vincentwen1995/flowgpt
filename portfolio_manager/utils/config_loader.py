import threading
import time
from pathlib import Path

import yaml

from .dynaconf_utils import settings

STRATEGY_CONFIGS_DIR = settings.STRATEGY_CONFIGS_DIR


class ConfigLoader:
    """
    A class for loading and managing configuration files.

    This class monitors the configuration files in the specified directory and reloads them periodically.

    Attributes:
        configs (dict): A dictionary storing the loaded configuration data.
        thread (Thread): A background thread for reloading the configurations.
    """

    def __init__(self):
        self.configs = {}
        self.thread = threading.Thread(target=self._reload_configs, daemon=True)

    def start(self):
        """
        Start the background thread for reloading configurations.
        """
        self.thread.start()

    def _reload_configs(self):
        """
        Internal method to reload configurations periodically.
        """
        while True:
            self.load_configs()
            time.sleep(10)  # Reload configs every 10 seconds

    def load_configs(self):
        """
        Load the configuration files from the specified directory.
        """
        for yaml_file in (
            Path(settings.ROOT_PATH_FOR_DYNACONF) / STRATEGY_CONFIGS_DIR
        ).glob("*yaml"):
            with open(yaml_file, "r") as file:
                config_data = yaml.safe_load(file)
                self.configs[yaml_file.stem] = config_data

    def get_config(self, config_name):
        """
        Get the configuration data for the specified configuration name.

        Args:
            config_name (str): The name of the configuration.

        Returns:
            dict: The configuration data as a dictionary. Returns an empty dictionary if the configuration is not found.
        """
        return self.configs.get(config_name, {})
