import json
from cytomat.scripts.setup_cytomat import get_config_dir

def lazy_load_config():
    try:
        config_file = get_config_dir() / 'config.json'
        with open(config_file, 'r') as f:
            python_data = json.load(f)
            return python_data
    except:
        print(f"config file: {config_file} not found")
        return None

python_data = lazy_load_config()

if python_data:
    steps_per_mm_h = python_data['steps_per_mm_h']
    max_steps_h = python_data['max_steps_h']
    steps_per_mm_x = python_data['steps_per_mm_x']
    max_steps_x = python_data['max_steps_x']
    steps_per_mm_shovel = python_data['steps_per_mm_shovel']
    max_steps_shovel = python_data['max_steps_shovel']
    steps_per_deg_turn = python_data['steps_per_deg_turn']
    max_deg_turn = python_data['max_deg_turn']
    lid_holder_slot = python_data['lid_holder_slot']
    pipet_station_slot = python_data['pipet_station_slot']
    COM_port = python_data['COM_port']
