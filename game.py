# Pygame environment test

# "Pong icon made by Freepik from www.flaticon.com"
# Based on freeCodeCamp.org pygame tutorial from: https://www.youtube.com/watch?v=FfWpgLFMI7w

import pygame
import constants as ct

# Initialize the game
pygame.init()

# Create a window
screen = pygame.display.set_mode((ct.WINDOW_WIDTH, ct.WINDOW_HEIGHT))
pygame.display.set_caption("Pong game")              # window title
icon = pygame.image.load('graphics/pong-icon.png')   # game icon, 32x32 png
pygame.display.set_icon(icon)

# Player - TO BE CONVERTED INTO AN OBJECT!
player1_x = ct.PONG_BAR_WALL_PADDING                # start position
player1_y = ct.WINDOW_HEIGHT/2-ct.PONG_BAR_HEIGHT/2
player2_x = ct.WINDOW_WIDTH - ct.PONG_BAR_WALL_PADDING - ct.PONG_BAR_WIDTH
player2_y = ct.WINDOW_HEIGHT / 2 - ct.PONG_BAR_HEIGHT / 2
player1_move_step = 0                                # move velocity - ONLY FOR KEYBOARD
player2_move_step = 0

# Draw player's paddle on a new position
def move_player(number, x, y):          # player-number (1 or 2), pos-x, pos-y
    y = max(0, y)                 # make sure y stays above 0 (screen boundary)
    y = min(y, ct.WINDOW_HEIGHT-ct.PONG_BAR_HEIGHT)  # make sure it does not got too much down

    if number == 1:     # red player
        pygame.draw.rect(screen, ct.RED, (x,y, ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    elif number == 2:   # blue player
        pygame.draw.rect(screen, ct.BLUE, (x, y, ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    else:
        print("Error! Move player can only accept 1 or two as player number.")

# Initialize game graphics such as background and players
def initialize_game():
    screen.fill(ct.WINDOW_BG_COLOR)  # screen background
    # Draw pong paddles
    pygame.draw.rect(screen, ct.RED, (ct.PONG_BAR_WALL_PADDING, ct.WINDOW_HEIGHT / 2 - ct.PONG_BAR_HEIGHT / 2, ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))  # upper-left corner as position ref
    pygame.draw.rect(screen, ct.BLUE, (ct.WINDOW_WIDTH - ct.PONG_BAR_WALL_PADDING - ct.PONG_BAR_WIDTH, ct.WINDOW_HEIGHT / 2 - ct.PONG_BAR_HEIGHT / 2, ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    pygame.display.update()  # refresh screen

initialize_game()                       # Initialize game graphics such as background and players

# Game loop
running = True
lastKey = ''
while running:
    screen.fill(ct.WINDOW_BG_COLOR)  # screen background

    for event in pygame.event.get():    # run through all events
        if event.type == pygame.QUIT:   # close button = quit event
            running = False             # stop the program by exiting the loop

        if event.type == pygame.KEYDOWN:  # Key pressed
            if event.key == pygame.K_w:                 # W-Key
                lastKey = 'w'
                player1_move_step = -0.6
            elif event.key == pygame.K_s:               # S-Key
                lastKey = 's'
                player1_move_step = 0.6
            elif event.key == pygame.K_UP:              # Up
                lastKey = 'up'
                player2_move_step = -0.6
            elif event.key == pygame.K_DOWN:            # Down
                lastKey = 'down'
                player2_move_step = 0.6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:   # Key released
                player1_move_step = 0                  # stop player 1
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_move_step = 0                  # stop player 2

    player1_y += player1_move_step
    player2_y += player2_move_step
    move_player(1, player1_x, player1_y)
    move_player(2, player2_x, player2_y)
    pygame.display.update()             # refresh screen