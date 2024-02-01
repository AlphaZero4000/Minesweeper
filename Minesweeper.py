import pygame as pg
import random

pg.init()

board = [[[0, 0] for x in range(13)] for x in range(13)] 
'''
First number represents number of mines in adjacent squares; -1 represents a mine
Second number: 0 is nothing, -1 is right click, 1 is left click
'''
NUM_MINES = 20

SQUARE_SIZE = 36
BORDER_WIDTH = 4

SCREEN_WIDTH = SQUARE_SIZE * len(board[0])
SCREEN_HEIGHT = SQUARE_SIZE * len(board)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLOR_1 = BLUE = (0, 0, 255)
COLOR_2 = GREEN = (0, 130, 0)
COLOR_3 = RED = (255, 0, 0)
COLOR_4 = DARK_BLUE = (0, 0, 134)
COLOR_5 = DARK_RED = (132, 0, 0)
COLOR_6 = TEAL = (0, 130, 132)
COLOR_7 = PURPLE = (132, 0, 132)
COLOR_8 = (117, 117, 117)
LIGHT_GRAY  = (240, 240, 240)
GRAY = (190, 190, 190)
DARK_GRAY = (130, 130, 130)
BLACK = (0, 0, 0)

screen.fill(GRAY)
pg.display.set_caption("Minesweeper")

def generate_board(row_clicked: int, col_clicked: int):
    num_mines_generated = 0
    while (num_mines_generated < NUM_MINES):
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        if board[row][col][0] == 0 and not ((row == row_clicked or row == row_clicked + 1 or row == row_clicked - 1) and (col == col_clicked or col == col_clicked + 1 or col == col_clicked - 1)):
            board[row][col][0] = -1
            num_mines_generated += 1
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c][0] != -1:
                if r >= 1 and board[r - 1][c][0] == -1:
                    board[r][c][0] += 1
                if c >= 1 and board[r][c - 1][0] == -1:
                    board[r][c][0] += 1
                if r >= 1 and c >= 1 and board[r - 1][c - 1][0] == -1:
                    board[r][c][0] += 1
                if r <= len(board) - 2 and board[r + 1][c][0] == -1:
                    board[r][c][0] += 1
                if c <= len(board[r]) - 2 and board[r][c + 1][0] == -1:
                    board[r][c][0] += 1
                if r <= len(board) - 2 and c <= len(board[r]) - 2 and board[r + 1][c + 1][0] == -1:
                    board[r][c][0] += 1
                if r <= len(board) - 2 and c >= 1 and board[r + 1][c - 1][0] == -1:
                    board[r][c][0] += 1
                if r >= 1 and c <= len(board[r]) - 2 and board[r - 1][c + 1][0] == -1:
                    board[r][c][0] += 1
    left_click(row_clicked, col_clicked)

def left_click(row: int, col: int):
    if board[row][col][1] != 0: return
    if board[row][col][0] > 0:
        board[row][col][1] = 1
        pg.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pg.draw.rect(screen, DARK_GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
        color = BLUE
        if (board[row][col][0] == 1): color = COLOR_1
        elif (board[row][col][0] == 2): color = COLOR_2
        elif (board[row][col][0] == 3): color = COLOR_3
        elif (board[row][col][0] == 4): color = COLOR_4
        elif (board[row][col][0] == 5): color = COLOR_5
        elif (board[row][col][0] == 6): color = COLOR_6
        elif (board[row][col][0] == 7): color = COLOR_7
        elif (board[row][col][0] == 8): color = COLOR_8
        font = pg.font.SysFont(None, 40, True)
        img = font.render(str(board[row][col][0]), True, color)
        screen.blit(img, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 5))
    elif board[row][col][0] == 0:
        generate_zero(row, col)
    elif board[row][col][0] == -1:
        lose(row, col)
    
def right_click(row: int, col: int):
    if board[row][col][1] == 1: return
    elif board[row][col][1] == -1:
        pg.draw.rect(screen, GRAY, (col * SQUARE_SIZE + BORDER_WIDTH + 1, row * SQUARE_SIZE + BORDER_WIDTH + 1, SQUARE_SIZE - 2 * BORDER_WIDTH - 2, SQUARE_SIZE - 2 * BORDER_WIDTH - 2))
        board[row][col][1] = 0
    else:
        board[row][col][1] = -1
        pg.draw.line(screen, BLACK, ((col + 0.5) * SQUARE_SIZE, (row + 0.5) * SQUARE_SIZE), ((col + 0.5) * SQUARE_SIZE, (row + 0.8) * SQUARE_SIZE), 3)
        pg.draw.polygon(screen, RED, [((col + 0.53) * SQUARE_SIZE, (row + 0.58) * SQUARE_SIZE), ((col + 0.53) * SQUARE_SIZE, (row + 0.26) * SQUARE_SIZE), ((col + 0.3) * SQUARE_SIZE, (row + 0.42) * SQUARE_SIZE)])
        pg.draw.line(screen, BLACK, ((col + 0.31) * SQUARE_SIZE, (row + 0.8) * SQUARE_SIZE), ((col + 0.69) * SQUARE_SIZE, (row + 0.8) * SQUARE_SIZE), 3)
        pg.draw.line(screen, BLACK, ((col + 0.39) * SQUARE_SIZE, (row + 0.72) * SQUARE_SIZE), ((col + 0.6) * SQUARE_SIZE, (row + 0.72) * SQUARE_SIZE), 3)
    
def generate_zero(row: int, col: int):
    if (board[row][col][0] != 0 or board[row][col][1] == 1):
        return
    pg.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pg.draw.rect(screen, DARK_GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
    board[row][col][1] = 1
    if row >= 1 and board[row - 1][col][1] != 1:
        if board[row - 1][col][0] == 0:
            generate_zero(row - 1, col)
        elif board[row - 1][col][0] > 0:
            left_click(row - 1, col)
    if col >= 1 and board[row][col - 1][1] != 1:
        if board[row][col - 1][0] == 0:
            generate_zero(row, col - 1)
        elif board[row][col - 1][0] > 0:
            left_click(row, col - 1)
    if row >= 1 and col >= 1 and board[row - 1][col - 1][1] != 1:
        if board[row - 1][col - 1][0] == 0:
            generate_zero(row - 1, col - 1)
        elif board[row - 1][col - 1][0] > 0:
            left_click(row - 1, col - 1)
    if row <= len(board) - 2 and board[row + 1][col][1] != 1:
        if board[row + 1][col][0] == 0:
            generate_zero(row + 1, col)
        elif board[row + 1][col][0] > 0:
            left_click(row + 1, col)
    if col <= len(board[row]) - 2 and board[row][col + 1][1] != 1:
        if board[row][col + 1][0] == 0:
            generate_zero(row, col + 1)
        elif board[row][col + 1][0] > 0:
            left_click(row, col + 1)
    if row <= len(board) - 2 and col <= len(board[row]) - 2 and board[row + 1][col + 1][1] != 1:
        if board[row + 1][col + 1][0] == 0:
            generate_zero(row + 1, col + 1)
        elif board[row + 1][col + 1][0] > 0:
            left_click(row + 1, col + 1)
    if row <= len(board) - 2 and col >= 1 and board[row + 1][col - 1][1] != 1:
        if board[row + 1][col - 1][0] == 0:
            generate_zero(row + 1, col - 1)
        elif board[row + 1][col - 1][0] > 0:
            left_click(row + 1, col - 1)
    if row >= 1 and col <= len(board[row]) - 2 and board[row - 1][col + 1][1] != 1:
        if board[row - 1][col + 1][0] == 0:
            generate_zero(row - 1, col + 1)
        elif board[row - 1][col + 1][0] > 0:
            left_click(row - 1, col + 1)

game_over = False
    
def lose(row: int, col: int):
    global game_over
    game_over = True
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c][0] == -1 and board[r][c][1] != -1:
                if r == row and c == col:
                    color = RED
                else: color = GRAY
                pg.draw.rect(screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pg.draw.rect(screen, DARK_GRAY, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

                pg.draw.circle(screen, BLACK, ((c + 0.5) * SQUARE_SIZE, (r + 0.5) * SQUARE_SIZE), 0.3 * SQUARE_SIZE)
                pg.draw.line(screen, BLACK, ((c + 0.25) * SQUARE_SIZE, (r + 0.25) * SQUARE_SIZE), ((c + 0.75) * SQUARE_SIZE, (r + 0.75) * SQUARE_SIZE), 3) #diagonals
                pg.draw.line(screen, BLACK, ((c + 0.75) * SQUARE_SIZE, (r + 0.25) * SQUARE_SIZE), ((c + 0.25) * SQUARE_SIZE, (r + 0.75) * SQUARE_SIZE), 3)
                pg.draw.line(screen, BLACK, ((c + 0.5) * SQUARE_SIZE, (r + 0.14) * SQUARE_SIZE), ((c + 0.5) * SQUARE_SIZE, (r + 0.86) * SQUARE_SIZE), 3) #vert/horiz
                pg.draw.line(screen, BLACK, ((c + 0.14) * SQUARE_SIZE, (r + 0.5) * SQUARE_SIZE), ((c + 0.86) * SQUARE_SIZE, (r + 0.5) * SQUARE_SIZE), 3)
                pg.draw.circle(screen, (225, 225, 225), ((c + 0.41) * SQUARE_SIZE, (r + 0.41) * SQUARE_SIZE), 0.06 * SQUARE_SIZE)
            elif board[r][c][1] == -1 and board[r][c][0] != -1:
                pg.draw.line(screen, RED, (c * SQUARE_SIZE + 5, r * SQUARE_SIZE + 4), ((c + 1) * SQUARE_SIZE - 6, (r + 1) * SQUARE_SIZE - 6), 3)
                pg.draw.line(screen, RED, ((c + 1) * SQUARE_SIZE - 6, r * SQUARE_SIZE + 4), (c * SQUARE_SIZE + 5, (r + 1) * SQUARE_SIZE - 6), 3)
    pg.display.update()

def win():
    global game_over
    if not first_move_done: return False
    for r in range(len(board)):
        for c in range(len(board[r])):
            if (board[r][c][0] > 0 and board[r][c][1] != 1):
                return False
    game_over = True
    return True

first_move_done = False
run = True

for r in range(len(board)):
        for c in range(len(board[r])):
            pg.draw.polygon(screen, LIGHT_GRAY, [(c * SQUARE_SIZE, r * SQUARE_SIZE), (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE), (c * SQUARE_SIZE + BORDER_WIDTH, (r + 1) * SQUARE_SIZE - BORDER_WIDTH), \
            (c * SQUARE_SIZE + BORDER_WIDTH, r * SQUARE_SIZE + BORDER_WIDTH), ((c + 1) * SQUARE_SIZE - BORDER_WIDTH, r * SQUARE_SIZE + BORDER_WIDTH), ((c + 1) * SQUARE_SIZE, r * SQUARE_SIZE)])
            pg.draw.polygon(screen, DARK_GRAY, [(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE), (c * SQUARE_SIZE + BORDER_WIDTH, (r + 1) * SQUARE_SIZE - BORDER_WIDTH), ((c + 1) * SQUARE_SIZE - BORDER_WIDTH, (r + 1) * SQUARE_SIZE - BORDER_WIDTH), \
            ((c + 1) * SQUARE_SIZE - BORDER_WIDTH, r * SQUARE_SIZE + BORDER_WIDTH), ((c + 1) * SQUARE_SIZE, r * SQUARE_SIZE), ((c + 1) * SQUARE_SIZE, (r + 1) * SQUARE_SIZE)])
pg.display.update()
    
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            x, y = pg.mouse.get_pos()
            if event.button == 1:        #left click
                if not first_move_done:
                    generate_board(int(y / SQUARE_SIZE), int(x / SQUARE_SIZE))
                    first_move_done = True
                else:
                    left_click(int(y / SQUARE_SIZE), int(x / SQUARE_SIZE))
            elif event.button == 3:      #right click
                right_click(int(y / SQUARE_SIZE), int(x / SQUARE_SIZE))
    if win():
        font = pg.font.SysFont(None, 100)
        img = font.render("You win", True, BLACK)
        screen.blit(img, (120, 120))
    pg.display.update()
pg.quit()




