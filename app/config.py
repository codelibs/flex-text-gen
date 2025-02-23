import yaml

def load_config(config_path="config.yaml"):
    """
    Load the YAML configuration file and return its contents as a dictionary.

    Parameters:
    config_path (str): Path to the YAML configuration file. Default is "config.yaml".
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config