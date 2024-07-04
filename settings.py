# adjust window size and FPS
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
FRAMERATE = 120

# adjust game speed
OBSTACLE_INTERVAL = 1300 # spawning speed of obstacles in ms
OBSTACLE_SPEED = 250
GROUND_SPEED = OBSTACLE_SPEED
BACKGROUND_SPEED = GROUND_SPEED * 0.8

# adjust gravity and jump height
GRAVITY = 800
JUMP_HEIGHT = 400

# adjust obstacle dimensions
OBSTACLE_SCALE_FACTOR = 1

# adjust difficulty levels
GAME_SPEED_FACTORS = [1, 1.5, 2]

'''
TO DO:
- add a new obstacle type similar to that in flappy bird
- implement 3 difficulty tiers as time passes: easy (<= 15) - medium (16 - 50) - hard (>= 51)
'''