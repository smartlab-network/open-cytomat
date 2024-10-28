import json
from cytomat.scripts.setup_cytomat import get_config_dir

def lazy_load_config():
    try:
        config_file = get_config_dir() / 'config.json'
        with open(config_file, 'r') as f:
            python_data = json.load(f)
            print("Data loaded")
            return python_data
    except:
        print("Data not loaded")
        print(f"config file: {config_file} not found")
        return None

class Parameters:
    def __init__(self):
        self.create_parameters()

    def create_parameters(self):
        python_data = lazy_load_config()
        if python_data:
            self.COM_port = python_data['COM_port']
            self.steps_per_mm_h = python_data['steps_per_mm_h']
            self.max_steps_h = python_data['max_steps_h']
            self.steps_per_mm_x = python_data['steps_per_mm_x']
            self.max_steps_x = python_data['max_steps_x']
            self.steps_per_mm_shovel = python_data['steps_per_mm_shovel']
            self.max_steps_shovel = python_data['max_steps_shovel']
            self.steps_per_deg_turn = python_data['steps_per_deg_turn']
            self.max_deg_turn = python_data['max_deg_turn']
            self.lid_holder_slot = python_data['lid_holder_slot']
            self.pipet_station_slot = python_data['pipet_station_slot']

def get_parameters():
    params = Parameters()
    return params