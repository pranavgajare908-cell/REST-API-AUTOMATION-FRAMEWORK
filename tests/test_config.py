from utils.config_reader import ConfigReader


def test_base_url():
    config = ConfigReader()
    
    base_url = config.get_base_url()
    print(f"Base URL: {base_url}")
    assert base_url == "https://api.qaautomationlabs.com/v1"
