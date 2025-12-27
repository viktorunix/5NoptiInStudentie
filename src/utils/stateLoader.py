import os


class stateLoader:
    @staticmethod
    def load_state() -> dict:
        loaded_state: dict = {}
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(dir + "/state/save.data", "r") as file:
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
        with open(dir + "/state/save.data", "w+") as file:
            file.write("night = 1")
        return loaded_state

    @staticmethod
    def advance_night(loaded_state: dict):
        loaded_state["night"] = str(int(loaded_state["night"]) + 1)
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(dir + "/state/save.data", "w+") as file:
            file.write("night = " + str(loaded_state["night"]))
        return loaded_state
