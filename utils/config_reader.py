import configparser
from pathlib import Path


class ConfigReader:

    def __init__(self):
        self.config = configparser.ConfigParser()

        project_root = Path(__file__).resolve().parent.parent
        self.config_file = project_root / "config" / "config.ini"

        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        self.config.read(self.config_file)

    def get_base_url(self):
        if not self.config.has_section("api"):
            raise ValueError(f"'[api]' section not found in: {self.config_file}")
        if not self.config.has_option("api", "base_url"):
            raise ValueError(f"'base_url' not found in [api] section of: {self.config_file}")
        return self.config.get("api", "base_url")