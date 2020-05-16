# Ball class
import random

class Ball:

    def __init__(self, radius):
        self.radius = radius
        self.position = [0, 0]   # ball position - ball center coordinates used
                                 # for rendering UL corner needs to be used -> see get_corner_position
        self.velocity = [0, 0]   # ball velocity [vx, vy]
        self.n_turns = 0         # counter of the number of hits by a player

        # Random start player allocation
        # -> start_player to be toggled after each first move in a round
        # -> after the first round the players take turns in starting
        self.start_player = random.randint(1,2)

    # Transform ball center position to GUI ball coordinates (UL-corner) and return them
    # For rendering purposes
    def get_corner_position(self):
        return (self.position[0] - self.radius , self.position[1] - self.radius)
