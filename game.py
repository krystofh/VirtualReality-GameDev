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
player1_x_start = ct.PONG_BAR_WALL_PADDING                # start position
player1_y_start = int(ct.WINDOW_HEIGHT/2)
player2_x_start = ct.WINDOW_WIDTH - ct.PONG_BAR_WALL_PADDING
player2_y_start = player1_y_start
player1 = Player("Krystof", 1, (player1_x_start, player1_y_start))  # Create players objects with initial position (paddle's center)
player2 = Player("Maciej", 2, (player2_x_start, player2_y_start))
player1_move_step = 0                                # move velocity - ONLY FOR KEYBOARD
player2_move_step = 0

# Create a ball
ball = Ball(ct.BALL_RADIUS)             # create a ball of defined radius


# Draw player's paddle on a new position
def move_player(player, x, y):          # player object, pos-x, pos-y
    # Save new position and get its UL corner coordinates
    player.position = [x, y]            # save player's new position (paddle's center)
    corner_position = player.get_corner_position()      # get UL corner coords

    # Keep players inside the window
    corner_position[1] = max(0, corner_position[1])     # make sure y stays above 0 (screen boundary)
    corner_position[1] = min(corner_position[1], ct.WINDOW_HEIGHT-ct.PONG_BAR_HEIGHT)  # make sure it does not got too much down

    # Render players
    if player.number == 1:     # red player
        pygame.draw.rect(screen, ct.RED, (corner_position[0],corner_position[1], ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    elif player.number == 2:   # blue player
        pygame.draw.rect(screen, ct.BLUE, (corner_position[0], corner_position[1], ct.PONG_BAR_WIDTH, ct.PONG_BAR_HEIGHT))
    else:
        print("Error move_player!")

# Draw ball on a new position
def move_ball(x, y):
    global ball
    # Save new position
    ball.position = [x, y]
    # Render (uses ball's center)
    pygame.draw.circle(screen, (200, 200, 200), ball.position, ball.radius)

# Initialize game graphics such as background and players
def initialize_game():
    global player1, player2, ball
    screen.fill(ct.WINDOW_BG_COLOR)  # screen background

    # Draw players (pong paddles) - positions already set up by object instantatiation
    move_player(player1, player1.position[0], player1.position[1])
    move_player(player2, player2.position[0], player2.position[1])

    # Draw ball object
    ball_x = 0
    ball_y = 0
    if ball.start_player == 1:
        print("Player 1 starts")
        ball_x = player1.position[0] + int(ct.PONG_BAR_WIDTH/2) + ball.radius
        ball_y = player1.position[1]
    elif ball.start_player == 2:
        print("Player 2 starts")
        ball_x = player2.position[0] - int(ct.PONG_BAR_WIDTH / 2) - ball.radius
        ball_y = player2.position[1]
    else:
        print("Error drawing ball on start position")
    move_ball(ball_x, ball_y)

    # Display score
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

            # Start ball
            if (event.key == pygame.K_w or event.key == pygame.K_s) and ball.start_player == 1:
                ball.velocity = [2, -2]   # start ball movement
            elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and ball.start_player == 2:
                ball.velocity = [-2, -2] # start ball movement

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:   # Key released
                player1_move_step = 0                  # stop player 1
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_move_step = 0                  # stop player 2

    # Add a move step to the positions
    player1.position[1] += player1_move_step
    player2.position[1] += player2_move_step
    # Ball movement
    ball.position[0] += ball.velocity[0]
    ball.position[1] += ball.velocity[1]

    # Refresh positions
    move_player(player1, player1.position[0], player1.position[1])
    move_player(player2, player2.position[0], player2.position[1])
    move_ball(ball.position[0], ball.position[1])

    # Score and screen update
    display_score()
    pygame.display.update()             # refresh screen