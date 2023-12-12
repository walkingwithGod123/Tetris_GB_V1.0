import pygame
from random import choice

# Game settings
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Tetrominoes shapes and colors
tetrominoes = [
    [[1, 1, 1, 1]],
    [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    [[0, 1, 0], [1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
]
tetromino_colors = [(0, 255, 255), (255, 128, 0), (255, 255, 0), (128, 0, 128), (255, 0, 0), (0, 255, 0), (128, 128, 128)]

# Game board
board = [
    [0 for _ in range(10)]
    for _ in range(22)
]

# Current tetromino and its position
curr_tetromino = None
curr_x = 3
curr_y = 0

# Rotation states for each tetromino
rotations = [
    [0],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
]

# Game state and score
game_over = False
score = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for game loop
clock = pygame.time.Clock()

def is_collision(board, tetromino, x, y):
    """
    Checks if the tetromino collides with the board or other tetrominoes.
    """
    for y_offset, row in enumerate(tetromino):
        for x_offset, cell in enumerate(row):
            if cell > 0:
                new_x = x + x_offset
                new_y = y + y_offset
                if new_x < 0 or new_x >= 10 or new_y >= 22 or board[new_y][new_x] > 0:
                    return True
    return False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                curr_x -= 1
            elif event.key == pygame.K_RIGHT:
                curr_x += 1
            elif event.key == pygame.K_DOWN:
                curr_y += 1
            elif event.key == pygame.K_SPACE:
                curr_tetromino = rotate_tetromino(curr_tetromino)
                if is_collision(board, curr_tetromino, curr_x, curr_y):
                    curr_tetromino = rotate_tetromino(curr_tetromino, reverse=True)

    # Update game logic
    if not game_over:
        # Check for collision and update position
        if is_collision(board, curr_tetromino, curr_x, curr_y + 1):
            # Lock the tetromino to the board
            merge_tetromino(board, curr_tetromino, curr_x, curr_y)
            # Check for line completion and remove lines
            lines_removed = remove_completed_lines(board)
            score += lines_removed * lines_removed * 100
            # Spawn new tetromino
            curr_tetromino = choice(tetrominoes)
            curr_x = 3
            curr_y = 0
        else:
            curr_y += 1

        # Check for game over condition
