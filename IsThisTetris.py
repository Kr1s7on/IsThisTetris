import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_WIDTH = 300  # Meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600  # Meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30

# Top left coordinates of the play area
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# Shapes
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(255, 255, 255)] * 7  # All shapes are white

# Define the shape class
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = (255, 255, 255)
        self.rotation = 0

# Create the grid
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

# Convert the shape format
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

# Check if the space is valid
def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Check if the game is lost
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Get a random shape
def get_shape():
    return Piece(5, 0, random.choice(shapes))

# Draw text in the middle of the screen
def draw_text_middle(text, size, color, surface, offset_y=0):
    font = pygame.font.SysFont('Arial', size, bold=True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 
                         TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2 + offset_y))

# Draw the grid
def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

# Clear rows that are filled up
def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    
    return increment

# Draw the next shape
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Arial', 20)
    label = font.render('Next Shape', 1, (255, 255, 255))
    
    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + 50
    
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    surface.blit(label, (start_x + 10, start_y - 30))

# Draw the held shape
def draw_held_shape(shape, surface):
    font = pygame.font.SysFont('Arial', 20)
    label = font.render('Held Shape', 1, (255, 255, 255))
    
    start_x = 50
    start_y = 180  # Increased to space out the text more
    
    if shape:
        format = shape.shape[shape.rotation % len(shape.shape)]
        
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    surface.blit(label, (start_x + 10, start_y - 30))

# Draw the game window
def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))
    
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20)
    font.set_bold(False)
    label = font.render('IsThisTetris', 1, (255, 255, 255))
    
    surface.blit(label, (50, 30))
    
    font = pygame.font.SysFont('Arial', 20)
    font.set_bold(False)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    
    surface.blit(label, (50, 100))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    draw_grid(surface, grid)
    
    pygame.draw.rect(surface, (255, 255, 255), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

# Main game loop
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    hold_piece = None
    hold_used = False
    clock = pygame.time.Clock()
    fall_time = 0
    
    score = 0
    
    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27
        
        fall_time += clock.get_rawtime()
        clock.tick()
        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_c:
                    if not hold_used:
                        if hold_piece is None:
                            hold_piece, current_piece = current_piece, next_piece
                            next_piece = get_shape()
                        else:
                            hold_piece, current_piece = current_piece, hold_piece
                            current_piece.x = 5
                            current_piece.y = 0
                        hold_used = True
        
        shape_pos = convert_shape_format(current_piece)
        
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            hold_used = False
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        draw_held_shape(hold_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            # Fill screen with black
            win.fill((0, 0, 0))
            
            # Display "YOU LOSE" in red text
            draw_text_middle("YOU LOSE", 60, (255, 0, 0), win)
            
            pygame.display.update()
            pygame.time.delay(1500)
            main_menu()
    
    pygame.display.quit()

# Main menu
def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('IsThisTetris', 60, (255, 255, 255), win, -50)
        draw_text_middle('Press Any Key To Start', 30, (255, 255, 255), win, 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

# Set up the display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('IsThisTetris')

# Start the game
main_menu()
