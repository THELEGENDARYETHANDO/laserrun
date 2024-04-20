def rotate_90_clockwise(matrix):
    """
    Rotate a 2D matrix by 90 degrees clockwise.
    
    Args:
    matrix (list of list): The input 2D matrix.
    
    Returns:
    list of list: The rotated matrix.
    """
    if not matrix or len(matrix) == 0:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Create a new matrix to store the rotated values
    rotated_matrix = [[0] * rows for _ in range(cols)]
    
    # Rotate the matrix
    for i in range(rows):
        for j in range(cols):
            rotated_matrix[j][rows - i - 1] = matrix[i][j]
    
    return rotated_matrix

# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
rotated_matrix = rotate_90_clockwise(matrix)
for row in rotated_matrix:
    print(row)

import pygame
# Initialize Pygame 
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Game Settings and Variables
SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 700
COLUMN_COUNT = 7
ROW_COUNT = 7
SQUARE_SIZE = 100

# Pygame Display Initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Connect 4')

# Game board
board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Player wins
player_wins = {1: 0, 2: 0}

# Function to draw the game board
def draw_board(board):
    board_width = COLUMN_COUNT * SQUARE_SIZE
    board_height = ROW_COUNT * SQUARE_SIZE

    # Calculate the position to center the board
    board_x = (SCREEN_WIDTH - board_width) // 2
    board_y = (SCREEN_HEIGHT - board_height) // 2

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (board_x + col * SQUARE_SIZE, board_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, WHITE, (board_x + col * SQUARE_SIZE, board_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)  # Draw grid lines
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    # Draw win counters
    win_counter_offset = 10
    for player, wins in player_wins.items():
        win_counter_text = font_small.render(f"Player {player} Wins: {wins}", True, BLACK)
        if player == 1:
            screen.blit(win_counter_text, (board_x - win_counter_text.get_width() - win_counter_offset, win_counter_offset))
        else:
            screen.blit(win_counter_text, (board_x + board_width + win_counter_offset, win_counter_offset))


def rotate_board_clockwise(board):
    print("hi")
    rows = len(board)
    columns = len(board[0])
    rotated_board = [[0]*rows for _ in range(columns)]
    for i in range(rows):
        for j in range(columns):
            rotated_board[j][rows - i - 1] = board[i][j]
    for row in rotated_board:
        print(row)
    print("")
    return rotated_board

# Token class
class Token:
    def __init__(self, color):
        self.color = color

    def place_token(self, board, mouse_x):
        col = mouse_x // SQUARE_SIZE  # Calculate the column based on the mouse click position
        if 0 <= col < COLUMN_COUNT:  # Check if column is within bounds
            for row in range(ROW_COUNT - 1, -1, -1):  # Iterate over rows from the bottom up
                if board[row][col] == 0:  # If the cell is empty in the clicked column
                    board[row][col] = self.color  # Place the token in that row
                    return row, col  # Return the position of the placed token
        return None, None  # Return None if token cannot be placed


# Token class
class Token:
    def __init__(self, color):
        self.color = color

    def place_token(self, board, col):
        for row in range(ROW_COUNT - 1, -1, -1):  # Iterate over rows from the bottom up
            if board[row][col] == 0:  # If the cell is empty in the clicked column
                board[row][col] = self.color  # Place the token in that row
                return row, col  # Return the position of the placed token
        return None, None  # Return None if column is full

    def check_win(self, board, row, col):
        # Check horizontally
        for c in range(col - 3, col + 1):
            if 0 <= c < COLUMN_COUNT - 3:
                if board[row][c] == board[row][c + 1] == board[row][c + 2] == board[row][c + 3] == self.color:
                    return True

        # Check vertically
        for r in range(row - 3, row + 1):
            if 0 <= r < ROW_COUNT - 3:
                if board[r][col] == board[r + 1][col] == board[r + 2][col] == board[r + 3][col] == self.color:
                    return True

        # Check diagonally (positive slope)
        for i in range(-3, 1):
            if 0 <= row + i < ROW_COUNT - 3 and 0 <= col + i < COLUMN_COUNT - 3:
                if board[row + i][col + i] == board[row + i + 1][col + i + 1] == board[row + i + 2][col + i + 2] == board[row + i + 3][col + i + 3] == self.color:
                    return True

        # Check diagonally (negative slope)
        for i in range(-3, 1):
            if 0 <= row - i < ROW_COUNT - 3 and 0 <= col + i < COLUMN_COUNT - 3:
                if board[row - i][col + i] == board[row - i - 1][col + i + 1] == board[row - i - 2][col + i + 2] == board[row - i - 3][col + i + 3] == self.color:
                    return True

        return False


# Main menu screen
def main_menu():
    screen.fill(BLACK)
    title_text = font_large.render("CONNECT 4", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

    play_button = font_medium.render("PLAY GAME", True, WHITE)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50))
    screen.blit(play_button, (SCREEN_WIDTH // 2 - play_button.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    pygame.display.update()

# Game over screen
def game_over_screen(winner):
    if winner == "Draw":
        winner_text = font_large.render("Draw", True, BLACK)
    else:
        winner_text = font_large.render(f"{winner} WINS!", True, BLACK)

    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 4))

    play_again_button = font_medium.render("PLAY AGAIN", True, WHITE)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50))
    screen.blit(play_again_button, (SCREEN_WIDTH // 2 - play_again_button.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    quit_button = font_medium.render("QUIT GAME", True, WHITE)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 50))
    screen.blit(quit_button, (SCREEN_WIDTH // 2 - quit_button.get_width() // 2, SCREEN_HEIGHT // 2 + 90))

    pygame.display.update()

# Main Game Loop
rungame = True
playing_game = False  # Flag to indicate if the game is currently being played
token1 = Token(1)  # Player 1's token (Red)
token2 = Token(2)  # Player 2's token (Yellow)
current_token = token1  # Start with player 1
game_over = False
winner = None

rotate_button = font_medium.render("ROTATE", True, BLACK)  # Black rotate button
rotate_button_rect = rotate_button.get_rect(topleft=(10, 10))

main_menu()
while rungame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not playing_game:
                    if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + 50:
                        # PLAY GAME button clicked
                        playing_game = True
                else:
                    if not game_over:
                        col = (mouse_x - (SCREEN_WIDTH - COLUMN_COUNT * SQUARE_SIZE) // 2) // SQUARE_SIZE  # Calculate the clicked column
                        row, col = current_token.place_token(board, col)
                        if row is not None and col is not None:  # Check if token was placed successfully
                            if current_token.check_win(board, row, col):
                                game_over = True
                                winner = "Player 1" if current_token == token1 else "Player 2"
                                player_wins[current_token.color] += 1
                            elif all(board[i][j] != 0 for i in range(ROW_COUNT) for j in range(COLUMN_COUNT)):
                                game_over = True
                                winner = "Draw"
                            current_token = token2 if current_token == token1 else token1
                    else:
                        if SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and SCREEN_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + 50:
                            # PLAY AGAIN button clicked
                            board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]  # Reset the board
                            game_over = False
                            winner = None
                        elif SCREEN_WIDTH // 2 - 150 < mouse_x < SCREEN_WIDTH // 2 + 150 and SCREEN_HEIGHT // 2 + 90 < mouse_y < SCREEN_HEIGHT // 2 + 140:
                            # QUIT GAME button clicked
                            rungame = False
        except:
            pass

    screen.fill(WHITE)
    if playing_game:
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_r]:
            # Rotate button clicked
            board = rotate_board_clockwise(board)
        draw_board(board)
        screen.blit(rotate_button, rotate_button_rect)  # Draw rotate button
    if game_over:
        game_over_screen(winner)
    if not playing_game:  # Display main menu if game is not being played
        main_menu()
    pygame.display.update()

pygame.quit()