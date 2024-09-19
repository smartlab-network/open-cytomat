import json

python_data = json.load(open('C:\labhub\Repos\smartlab-network\open-cytomat\src\cytomat\cytomat.json'))

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
