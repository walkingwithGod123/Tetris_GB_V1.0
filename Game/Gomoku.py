import pygame
import sys

# 游戏初始化
pygame.init()

# 设置窗口、标题和字体
width, height = 450, 480  # 窗口高度增加以适应顶部文字
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("五子棋")
font = pygame.font.Font(None, 24)

# 颜色定义
black = (0, 0, 0)
white = (255, 255, 255)
wood = (193, 154, 107)
light_wood = (238, 198, 150)

# 棋盘和棋子状态
board = [[0 for _ in range(15)] for _ in range(15)]
player = 1  # 1代表黑子，2代表白子
game_over = False

# 绘制棋盘
def draw_board(screen):
    screen.fill(wood)
    for i in range(15):
        pygame.draw.line(screen, black, (15 + i * 30, 45), (15 + i * 30, height - 15))
        pygame.draw.line(screen, black, (15, 45 + i * 30), (width - 15, 45 + i * 30))

    # 添加行号和列号
    for i in range(15):
        row_label = font.render(str(i + 1), True, black)
        col_label = font.render(chr(65 + i), True, black)
        screen.blit(row_label, (5, 40 + i * 30))
        screen.blit(col_label, (12 + i * 30, 10))

    # 绘制棋子
    for i in range(15):
        for j in range(15):
            if board[i][j] != 0:
                color = black if board[i][j] == 1 else white
                pygame.draw.circle(screen, color, (15 + j * 30, 45 + i * 30), 10)

# 检查获胜者
def check_winner(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            if 0 <= x + dx * i < 15 and 0 <= y + dy * i < 15 and board[x + dx * i][y + dy * i] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            if 0 <= x - dx * i < 15 and 0 <= y - dy * i < 15 and board[x - dx * i][y - dy * i] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = (y - 45) // 30, x // 30
            if 0 <= row < 15 and 0 <= col < 15 and board[row][col] == 0:
                board[row][col] = player
                if check_winner(row, col, player):
                    game_over = True
                    print(f"Player {player} wins!")
                player = 3 - player

    draw_board(screen)

    # 顶部文字提示
    player_text = font.render(f"玩家1：黑子，玩家2：白子", True, black)
    screen.blit(player_text, (10, 10))

    pygame.display.flip()
