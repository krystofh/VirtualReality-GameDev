# Python class Player
import constants as ct

class Player:

    def __init__(self, name, number, initial_pos):
        self.name = name
        self.number = number
        self.score = 0
        self.position = initial_pos    # Position of a player defined as the center of the paddle (bar)
                                       # rendering uses UL corner (-> see get_corner_position)

    def get_corner_position(self):
        corner_position = [self.position[0] - int(ct.PONG_BAR_WIDTH/2), self.position[1] - int(ct.PONG_BAR_HEIGHT/2)]
        return corner_position