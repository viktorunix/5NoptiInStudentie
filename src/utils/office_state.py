from enum import Enum, auto


class office_state(Enum):
    # TODO: add more states
    OFFICE_FRONT_LIGHTS = auto()
    OFFICE_FRONT_DARK = auto()
    OFFICE_BACK_LIGHTS = auto()
    OFFICE_BACK_DARK = auto()
    CAMERA_SCREEN = auto()
    OFFICE_FRONT_LIGHTS_OPEN = auto()
    OFFICE_FRONT_DARK_OPEN = auto()
    OFFICE_BACK_LIGHTS_OPEN = auto()
    OFFICE_BACK_DARK_OPEN = auto()
