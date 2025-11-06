import random as rd

class BigBug:
    __state = 0
    __backward_probs = [0, 0.24, 0.5, 0.25]
    __forward_probs = [0.12, 0.24, 0.05, 0.4]
    def __init__(self):
        self.__state = 0
        for i in range(3):
            self.__forward_probs[i] = 1 - self.__forward_probs[i]
    def getstate(self):
        return self.__state
    def setstate(self, state):
        self.__state = state
    def change_state(self):
        num = rd.random()
        if num < self.__backward_probs[self.__state]:
            self.__state -= 1
            return
        if num > self.__forward_probs[self.__state]:
            self.__state += 1
        return
