import random

from mechanics.clock import clock
from utils.camera_state import camera_state


class BigBug:
    def __init__(self, name: str, start_pos: camera_state, ai_level: int):
        self.name = name
        self.location = start_pos
        self.ai_level = ai_level
        self.move_timer = 0
        self.move_interval = 300  # 300 ticks or 5 seconds

        # the path of the bug current_location->list of possible locations

        self.path_network = {
            camera_state.BATHROOM_HALLWAY: [camera_state.MAIN_HALLWAY_A],
            camera_state.MAIN_HALLWAY_A: [
                camera_state.STAIRWAY,
                camera_state.MAIN_HALLWAY_B,
            ],
            camera_state.STAIRWAY: [camera_state.MAIN_HALLWAY_B],
            camera_state.MAIN_HALLWAY_B: [camera_state.MAIN_HALLWAY_OFFICE],
            camera_state.MAIN_HALLWAY_OFFICE: [camera_state.NONE],
            camera_state.NONE: [],  # jumpscare here
        }

    def update(self):
        """called once per frame in the game"""
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.attempt_move()

    def attempt_move(self):
        """The main AI logic: rolls a 20 faced dice.
        If the face value is less than the AI level then the bug will move"""
        roll = random.randint(1, 20)
        print(f"[{self.name}] Rolled {roll} vs AI {self.ai_level}")
        if roll <= self.ai_level:
            self.move()

    def move(self):
        possible_moves = self.path_network.get(self.location, [])
        if possible_moves:
            next_room = random.choice(possible_moves)
            print(f"[{self.name}] Moving from {self.location} to {next_room}")
            self.location = next_room

            if self.location == camera_state.NONE:
                self.trigger_jumpscare()

    def trigger_jumpscare(self):
        print("JUMPSCARE")

    def set_ai_level(self, level):
        self.ai_level = level

    def get_location(self) -> camera_state:
        return self.location

    def force_retreat(self, target_room: camera_state):
        print(f"[{self.name}] REPELLED! Moved back to {target_room}")
        self.location = target_room
        self.move_timer = 0
