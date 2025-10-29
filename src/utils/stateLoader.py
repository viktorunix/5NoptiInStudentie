import os
class stateLoader:

    def loadState():
        loaded_state: dict = {}
        dir: str = os.path.dirname(os.path.abspath(__file__))
        dir = dir[:-10]
        with open(dir + "/state/save.data", "r") as file:
            raw_data = file.read()
            data = raw_data.split()
            loaded_state[data[0]] = data[2]
        return loaded_state

