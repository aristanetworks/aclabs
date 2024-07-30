import yaml
import json

def yaml_to_json(yaml_file_path, json_file_path):
    """Converts a YAML file to a JSON file.

    Args:
        yaml_file_path (str): The path to the input YAML file.
        json_file_path (str): The path to the output JSON file.
    """

    with open(yaml_file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)  # Safely load YAML

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Format JSON with indentation

# Example Usage:
yaml_file_path = "act/act_topology.yml"
json_file_path = "act/act_topology.json"

yaml_to_json(yaml_file_path, json_file_path)
