# Pygame environment test

# "Pong icon made by Freepik from www.flaticon.com"
# Based on freeCodeCamp.org pygame tutorial from: https://www.youtube.com/watch?v=FfWpgLFMI7w
import pygame
from pygame import mixer
import random
import math
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

# Load sounds
mixer.pre_init()
mixer.init(size = -8, channels=1, buffer = 512)
bounce_sound = mixer.Sound("sounds/bounce.wav")

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
    # Keep ball inside the window
    ball.position[1] = max(0 + ball.radius, ball.position[1])
    ball.position[1] = min(ct.WINDOW_HEIGHT - ball.radius, ball.position[1])
    # Render (uses ball's center)
    pygame.draw.circle(screen, (200, 200, 200), ball.position, ball.radius)

# Initialize game graphics such as background and players
def initialize_game():
    global player1, player2, ball
    global player1_x_start, player1_y_start, player2_x_start, player1_y_start

    screen.fill(ct.WINDOW_BG_COLOR)  # screen background
    # Reset players' positions
    player1.position = [player1_x_start, player1_y_start]
    player2.position = [player2_x_start, player2_y_start]
    # Draw players (pong paddles)
    move_player(player1, player1.position[0], player1.position[1])
    move_player(player2, player2.position[0], player2.position[1])

    # Random start player
    if ball.start_player == 1:
        ball.start_player = 2
    else:
        ball.start_player = 1
    #                ball.start_player = random.randint(1, 2)
    # Reset n_turns (player's hit counter)
    ball.n_turns = 0
    # Set velocity to 0
    ball.velocity = [0, 0]

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

# Check goal
def check_goal():
    global player1, player2, ball
    if ball.position[0] == ball.radius:    # player 2 scored (left field border reached)
        # Play goal sound
        goal_sound = mixer.Sound("sounds/goal.wav")
        goal_sound.play()
        print("Player 2 scored")
        player2.score += 1   # update player's score
        initialize_game()
    elif ball.position[0] == ct.WINDOW_WIDTH - ball.radius:  # player 1 scored (right border reached)
        # Play goal sound
        goal_sound = mixer.Sound("sounds/goal.wav")
        goal_sound.play()
        print("Player 1 scored")
        player1.score += 1    # update player's score
        initialize_game()

# Check bounce from a wall
def check_bounce():
    global ball, bounce_sound
    if ball.position[1] == ball.radius or ball.position[1] == (ct.WINDOW_HEIGHT - ball.radius):
        # Bounce sound
        bounce_sound.play()
        # Change velocity: ball center at the top or bottom window edge
        ball.velocity[1] = ball.velocity[1] * (-1)   # revert vy sign


# Check paddle's hit
def check_hit():
    global player1, player2, ball, bounce_sound
    dmax = math.sqrt((ball.radius + int(ct.PONG_BAR_WIDTH/2))**2 + (ball.radius + int(ct.PONG_BAR_HEIGHT/2))**2)
    players = (player1, player2)
    if not ball.n_turns == 0:
        # Check if player hit
        for player in players:
            if abs(ball.position[0] - player.position[0]) == (ball.radius + int(ct.PONG_BAR_WIDTH/2)) and \
            math.sqrt((ball.position[0] - player.position[0])**2 + (ball.position[1] - player.position[1])**2) <= dmax:
                # Bounce sound
                bounce_sound.play()
                print("Player {} hit!".format(player.number))
                ball.velocity[0] = ball.velocity[0] * (-1) # revert vx sign to bounce off
                ball.n_turns += 1

# Kick-off
def kickoff(player_n, direction):   # player number, direction "up"/"down"
    global ball, player1, player2
    factor = random.uniform(0.45, 0.55)  # random factor for velocity generation
    ball.n_turns += 1  # hit counter

    if direction == "up":
        ball.velocity[1] = factor * ct.BALL_SPEED
    elif direction == "down":
        ball.velocity[1] = - factor * ct.BALL_SPEED
    else:
        print("Error kicking off")

    if player_n == 1:
        ball.velocity[0] = (1 - factor) * ct.BALL_SPEED
    elif player_n == 2:
        ball.velocity[0] = - (1 - factor) * ct.BALL_SPEED
    else:
        print("Error kicking off")
    print("Ball velocity: {},{}".format(ball.velocity[0], ball.velocity[1]))

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

            # Start ball (kick off)
            if ball.n_turns == 0:
                if ball.start_player == 1:
                    if event.key == pygame.K_w:
                        ball.velocity[0] = ct.BALL_SPEED
                        ball.velocity[1] = -ct.BALL_SPEED
                        #kickoff(1, "up")
                    elif event.key == pygame.K_s:
                        ball.velocity[0] = ct.BALL_SPEED
                        ball.velocity[1] = ct.BALL_SPEED
                        #kickoff(1, "down")
                elif ball.start_player == 2:
                    if event.key == pygame.K_UP:
                        ball.velocity[0] = -ct.BALL_SPEED
                        ball.velocity[1] = -ct.BALL_SPEED
                        #kickoff(2, "up")
                    elif event.key == pygame.K_DOWN:
                        ball.velocity[0] = -ct.BALL_SPEED
                        ball.velocity[1] = ct.BALL_SPEED
                        #kickoff(2, "down")
                ball.n_turns += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:   # Key released
                player1_move_step = 0                  # stop player 1
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_move_step = 0                  # stop player 2

    # Add a move step to the positions
    player1.position[1] += player1_move_step
    player2.position[1] += player2_move_step
    # Ball movement
    ball.position[0] = int(ball.position[0] + ball.velocity[0])
    ball.position[1] = int(ball.position[1] + ball.velocity[1])

    # Refresh positions
    move_player(player1, player1.position[0], player1.position[1])
    move_player(player2, player2.position[0], player2.position[1])
    move_ball(ball.position[0], ball.position[1])

    # Check events
    check_goal()
    check_bounce()
    check_hit()

    # Score and screen update
    display_score()
    pygame.display.update()             # refresh screen