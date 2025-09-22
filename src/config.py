from pathlib import Path
import yaml

def load_config(config_path=None):
    if config_path is None:
        config_path = Path(__file__).parent  / "settings.yaml"
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config