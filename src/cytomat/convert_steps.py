from cytomat.parameters import Parameters


class ConvertSteps:
    parameters = Parameters()
    parameters.load()

    @classmethod
    def mm_to_steps_x(cls, mm: float) -> int:
        return round(cls.parameters.steps_per_mm_x * mm)

    @classmethod
    def steps_to_mm_x(cls, steps: int) -> float:
        return round(1 / (cls.parameters.steps_per_mm_x / steps), 4)

    @classmethod
    def mm_to_steps_h(cls, mm: float) -> int:
        return round(cls.parameters.steps_per_mm_h * mm)

    @classmethod
    def steps_to_mm_h(cls, steps: int) -> float:
        return round(1 / (cls.parameters.steps_per_mm_h / steps), 4)

    @classmethod
    def mm_to_steps_shovel(cls, mm: float) -> int:
        return round(cls.parameters.steps_per_mm_shovel * mm)

    @classmethod
    def steps_to_mm_shovel(cls, steps: int) -> float:
        return round(1 / (cls.parameters.steps_per_mm_shovel / steps), 4)

    @classmethod
    def deg_to_steps_turn(cls, deg: float) -> int:
        return round(cls.parameters.steps_per_deg_turn * deg)

    @classmethod
    def steps_to_deg_turn(cls, steps: int) -> float:
        return round(1 / (cls.parameters.steps_per_deg_turn / steps), 4)
