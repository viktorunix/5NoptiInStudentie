import os
import sys


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    if relative_path.startswith("/") or relative_path.startswith("\\"):
        relative_path = relative_path[1:]
    return os.path.join(base_path, relative_path)


class stateLoader:
    @staticmethod
    def load_state() -> dict:
        loaded_state: dict = {}
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(get_resource_path("/state/save.data"), "r") as file:
            raw_data = file.read()
            data = raw_data.split()
            loaded_state[data[0]] = data[2]
        return loaded_state

    @staticmethod
    def new_state() -> dict:
        loaded_state: dict = {}
        loaded_state["night"] = 1
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(get_resource_path("/state/save.data"), "w+") as file:
            file.write("night = 1")
        return loaded_state

    @staticmethod
    def advance_night(loaded_state: dict):
        loaded_state["night"] = str(int(loaded_state["night"]) + 1)
        if int(loaded_state["night"]) >= 5:
            loaded_state["night"] = "5"
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(get_resource_path("/state/save.data"), "w+") as file:
            file.write("night = " + str(loaded_state["night"]))
        return loaded_state
