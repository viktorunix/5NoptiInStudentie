import random as rd

class BigBug:
    def __init__(self):
        self.__state = 0
        self.__backwardProbs = [0, 0.24, 0.5, 0.25]
        self.__forwardProbs = [0.12, 0.24, 0.05, 0.4]
        for i in range(4):
            self.__forwardProbs[i] = 1 - self.__forwardProbs[i]
    def getstate(self):
        return self.__state
    def setstate(self, state):
        self.__state = state
    def change_state(self):
        num = rd.random()
        if num < self.__backwardProbs[self.__state]:
            self.__state -= 1
            return
        if num > self.__forwardProbs[self.__state]:
            self.__state += 1
        return
