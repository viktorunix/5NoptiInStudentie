class OxygenMeter:

    def __init(self):
        self.level = 100;
        self.usage = 0;

    def update(self, dt, spray_use):
        self.usage = 1;
        self.usage += spray_use

        self.level -= self.usage * dt * 0.25
        self.level = 0 if self.level < 0 else self.level
