class clock:
    """Tracks time to update mechanic and to see night progress"""

    def __init__(self):
        self.__ticks = 0
        self.__seconds = 0
        self.__minutes = 0

    def get_tick(self):
        return self.__ticks

    def get_seconds(self):
        return self.__seconds

    def get_minutes(self):
        return self.__minutes

    def update(self):
        self.__ticks += 1
        if self.__ticks == 60:
            self.__seconds += 1
            self.__ticks = 0
        if self.__seconds == 60:
            self.__minutes += 1
            self.__seconds = 0

    def get_hour_text(self) -> str:
        if self.__minutes == 0:
            return "12"
        else:
            return "0" + str(self.__minutes)
