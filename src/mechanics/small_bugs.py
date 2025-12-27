class small_bugs:
    def __init__(self, limit: int, amount_remove: int):
        self.limit = limit
        self.current_bugs = 0
        self.amount_remove = amount_remove

        self.move_timer = 0
        self.move_interval = 30  # 30 ticks or half a second

    def update(self):
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.increase_counter()

    def increase_counter(self):
        self.current_bugs += 1
        if self.current_bugs > self.limit:
            self.current_bugs = self.limit

    def decrease_counter(self):
        self.current_bugs -= self.amount_remove
        if self.current_bugs < 0:
            self.current_bugs = 0

    def check_limit(self) -> bool:
        return self.current_bugs >= self.limit
