from cytomat.utils import lazy_load_config_file


class Parameters:

    @classmethod
    def load(cls):
        python_data = lazy_load_config_file()
        if python_data:
            cls.COM_port = python_data["COM_port"]
            cls.steps_per_mm_h = python_data["steps_per_mm_h"]
            cls.max_steps_h = python_data["max_steps_h"]
            cls.steps_per_mm_x = python_data["steps_per_mm_x"]
            cls.max_steps_x = python_data["max_steps_x"]
            cls.steps_per_mm_shovel = python_data["steps_per_mm_shovel"]
            cls.max_steps_shovel = python_data["max_steps_shovel"]
            cls.steps_per_deg_turn = python_data["steps_per_deg_turn"]
            cls.max_deg_turn = python_data["max_deg_turn"]
            cls.lid_holder_slot = python_data["lid_holder_slot"]
            cls.pipet_station_slot = python_data["pipet_station_slot"]
            cls.measurement_slot = python_data["measurement_slot"]
