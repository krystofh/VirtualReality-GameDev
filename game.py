# Pygame environment test

# "Pong icon made by Freepik from www.flaticon.com"
# Based on freeCodeCamp.org pygame tutorial from: https://www.youtube.com/watch?v=FfWpgLFMI7w

import pygame
import constants as ct
from Player import Player
from Ball import Ball

# Initialize the game
pygame.init()

# Create a window
screen = pygame.display.set_mode((ct.WINDOW_WIDTH, ct.WINDOW_HEIGHT))
pygame.display.set_caption("Pong game")              # window title
icon = pygame.image.load('graphics/pong-icon.png')   # game icon, 32x32 png
pygame.display.set_icon(icon)

# Create players
player1_x = ct.PONG_BAR_WALL_PADDING                # start position
player1_y = int(ct.WINDOW_HEIGHT/2)
player2_x = ct.WINDOW_WIDTH - ct.PONG_BAR_WALL_PADDING
player2_y = player1_y
player1 = Player("Krystof", 1, (player1_x, player1_y))  # Create players objects with initial position (paddle's center)
player2 = Player("Maciej", 2, (player2_x, player2_y))
player1_move_step = 0                                # move velocity - ONLY FOR KEYBOARD
player2_move_step = 0

# Create a ball
ball = Ball(ct.BALL_RADIUS)             # create a ball of defined radius


# Draw player's paddle on a new position
def move_player(player, x, y):          # player object, pos-x, pos-y
    player.position = [x, y]            # save player's new position (paddle's center)
    corner_position = player.get_corner_position()      # get UL corner coords
    corner_position[1] = max(0, corner_position[1])     # make sure y stays above 0 (screen boundary)
    corner_position[1] = min(corner_position[1], ct.WINDOW_HEIGHT-ct.PONG_BAR_HEIGHT)  # make sure it does not got too much down

    if player.number == 1:     # red player
        pygame.draw.rect(screen, ct.RED, (corner_position[0],corner_position[1], ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    elif player.number == 2:   # blue player
        pygame.draw.rect(screen, ct.BLUE, (corner_position[0], corner_position[1], ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    else:
        print("Error move_player!")

def move_ball(x, y):
    pygame.draw.circle(screen, (200, 200, 200), (x, y), ct.BALL_RADIUS)


# Initialize game graphics such as background and players
def initialize_game():
    global player1, player2
    screen.fill(ct.WINDOW_BG_COLOR)  # screen background
    # Draw pong paddles
    move_player(player1, player1.position[0], player1.position[1])
    move_player(player2, player2.position[0], player2.position[1])
    move_ball(100, 100)
    display_score()
    pygame.display.update()  # refresh screen

# Display players' score
def display_score():
    global player1, player2

    score_font = pygame.font.Font('freesansbold.ttf', 25)
    score1 = score_font.render('Player 1: ' + str(player1.score), True, (255, 255, 255))
    score2 = score_font.render('Player 2: ' + str(player2.score), True, (255, 255, 255))
    screen.blit(score1, (ct.PONG_BAR_WALL_PADDING+ct.PONG_BAR_WIDTH+50,30))
    screen.blit(score2, (ct.WINDOW_WIDTH-ct.PONG_BAR_WALL_PADDING-ct.PONG_BAR_WIDTH-score2.get_size()[0]-50, 30))

initialize_game()                       # Initialize game graphics such as background and players

# Game loop
running = True
while running:
    screen.fill(ct.WINDOW_BG_COLOR)  # screen background

    for event in pygame.event.get():    # run through all events
        if event.type == pygame.QUIT:   # close button = quit event
            running = False             # stop the program by exiting the loop

        if event.type == pygame.KEYDOWN:  # Key pressed
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:                 # W-Key
                player1_move_step = -ct.PLAYER_SPEED
            elif event.key == pygame.K_s:               # S-Key
                player1_move_step = ct.PLAYER_SPEED
            elif event.key == pygame.K_UP:              # Up
                player2_move_step = -ct.PLAYER_SPEED
            elif event.key == pygame.K_DOWN:            # Down
                player2_move_step = ct.PLAYER_SPEED

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:   # Key released
                player1_move_step = 0                  # stop player 1
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_move_step = 0                  # stop player 2

    player1_y += player1_move_step
    player2_y += player2_move_step
    move_player(player1, player1_x, player1_y)
    move_player(player2, player2_x, player2_y)
    move_ball(100, 100)
    display_score()
    pygame.display.update()             # refresh screen