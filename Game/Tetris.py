import pygame
import random

# 初始化pygame
pygame.init()
pygame.mixer.init()
# 引入像素字体文件
font_path = 'F:\Python Project\Game\Font_Press_Start_2P\Press_Start_2P\PressStart2P-Regular.ttf'  # 请替换为你的字体文件路径
# 在初始化部分加载字体
font = pygame.font.Font(font_path, 32)  # 第二个参数是字号

# 加载并播放背景音乐
# pygame.mixer.music.load('F:\Python Project\TerisEliminate.MP3')  # 替换为您的音乐文件路径
# pygame.mixer.music.play(-1)  # 循环播放

Title_sound = pygame.mixer.Sound('F:/Python Project/Game/Title.mp3')  # 加载游戏主界面音乐
Playing_sound = pygame.mixer.Sound('F:/Python Project/Game/Tetris.MP3')  # 加载游戏运行时音乐
line_clear_sound = pygame.mixer.Sound('F:/Python Project/Game/TerisEliminate.mp3')  # 加载方块消除音乐
line_clear_sound.set_volume(1.0)  # 设置音量
GameOver_sound = pygame.mixer.Sound('F:/Python Project/Game/Game Over.mp3')  # 加载游戏结束音乐

# # 播放游戏运行音乐
# Playing_sound.set_volume(0.1)
# Playing_sound.play(-1)

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (192, 192, 192)  # 用于方块的灰色
LIGHT_GREY = (199, 208, 208)  # 用于背景的淡灰色

# 设置游戏界面窗口大小
SCREEN_WIDTH, SCREEN_HEIGHT = 540, 600  # 更小的屏幕，留出空间显示游戏信息
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 定义方块移动区域和方块大小和
GAME_WIDTH, GAME_HEIGHT = 300, 600  # 方块移动区域大小
GAME_X, GAME_Y = 0, 0  # 方块移动区域的位置
BLOCK_SIZE = 30
# 设置分界线的颜色和宽度
BORDER_COLOR = (0, 0, 0)  # 红色
BORDER_WIDTH = 4  # 宽度为4像素
# 定义基本信息显示区域的位置和大小
info_area_x = GAME_WIDTH + BORDER_WIDTH  # 它从游戏区域和边界的右侧开始
info_area_y = 0  # 它从屏幕顶部开始
info_area_width = SCREEN_WIDTH - info_area_x  # 屏幕剩余的宽度
info_area_height = SCREEN_HEIGHT  # 屏幕的完整高度
# 定义小的信息显示框的颜色和间距
info_box_color1 = LIGHT_GREY
info_box_color2 = BLACK
info_box_color3 = LIGHT_GREY
padding = 20  # 内边距
info_box_spacing = 5  # 框之间的间距
# 分数框
score_box_x = info_area_x + padding
score_box_y = padding
score_box_width = info_area_width - 2 * padding
score_box_height = 100
# 等级框
level_box_y = score_box_y + score_box_height + info_box_spacing + 40
# 消除行数框
lines_box_y = level_box_y + score_box_height + info_box_spacing + 40
# 下一个形状框
next_shape_box_y = lines_box_y + score_box_height + info_box_spacing + 40
next_shape_box_height = 120  # 高度可能需要调整以适应形状的显示
# 定义背景框圆角矩形的半径
corner_radius = 6

# 定义一个新的全局变量来跟踪消除的行数
total_lines_removed = 0

# 设置游戏标题
pygame.display.set_caption("Tetris")

# 定义俄罗斯方块的形状
SHAPES = [
    [[1, 1, 1, 1]],  # 长条形
    [[1, 1, 1], [0, 1, 0]],  # T形
    [[1, 1], [1, 1]],  # 方块
    [[1, 0], [1, 1], [1, 0]],  # Z形
    [[0, 1, 1], [1, 1, 0]],  # S形
    [[1, 1, 0], [0, 1, 1]],  # 反Z形
    [[0, 1, 0], [1, 1, 1]],  # 反T形
    [[1, 0, 0], [1, 1, 1]],  # L形
    [[0, 0, 1], [1, 1, 1]]  # 反L形
]

# 定义一个二维数组来表示游戏区域
grid = [[0 for _ in range(GAME_WIDTH // BLOCK_SIZE)] for _ in range(GAME_HEIGHT // BLOCK_SIZE)]


# 游戏结束的条件和逻辑（简化版）
def game_over():
    return any(grid[0])


# 旋转形状的函数
def rotate(shape, position):
    rotated_shape = [list(row) for row in zip(*shape[::-1])]
    pos_x, pos_y = position
    for x, y in convert_shape_format(rotated_shape, position):
        if x < 0:
            pos_x += 1
        elif x >= GAME_WIDTH // BLOCK_SIZE:
            pos_x -= 1
    return rotated_shape, (pos_x, pos_y)


# 用于调整旋转后方块的位置，以防止它旋转到游戏区域外
def adjust_shape_position(shape, position):
    # Adjust the shape position if it goes beyond the left or right boundary
    pos_x, pos_y = position
    for x, y in convert_shape_format(shape, position):
        if x < 0:
            pos_x += 1
        elif x >= GAME_WIDTH // BLOCK_SIZE:
            pos_x -= 1
    return pos_x, pos_y


# 新增一个函数用来显示下一个方块
def display_next_shape(shape, surface):
    # 计算显示位置
    display_x = SCREEN_WIDTH - 160
    display_y = SCREEN_HEIGHT - 120
    # 渲染标题文字
    # text = font.render('Next:', True, BLACK)
    # surface.blit(text, (330, display_y - 40))  # 调整文字位置
    # 在这个位置绘制下一个方块的显示
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                # pygame.draw.rect(surface, LIGHT_GREY,
                #                  (display_x + x * BLOCK_SIZE, display_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # pygame.draw.rect(surface, BLACK,
                #                  (display_x + x * BLOCK_SIZE + 1, display_y + y * BLOCK_SIZE + 1, BLOCK_SIZE - 5, BLOCK_SIZE - 5))
                pygame.draw.rect(surface, BLACK,
                                 (display_x + x * BLOCK_SIZE, display_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, LIGHT_GREY,
                                 (display_x + x * BLOCK_SIZE + 2, display_y + y * BLOCK_SIZE + 2, BLOCK_SIZE - 6,
                                  BLOCK_SIZE - 6))
                pygame.draw.rect(surface, BLACK,
                                 (display_x + x * BLOCK_SIZE + 5, display_y + y * BLOCK_SIZE + 5, BLOCK_SIZE - 12,
                                  BLOCK_SIZE - 12))


# 给每个小方块添加一个边框，通过绘制一个略小于方块的矩形来实现这一点
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (GAME_X + x * BLOCK_SIZE, GAME_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, LIGHT_GREY,
                     (GAME_X + x * BLOCK_SIZE + 2, GAME_Y + y * BLOCK_SIZE + 2, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
    pygame.draw.rect(screen, BLACK,
                     (GAME_X + x * BLOCK_SIZE + 5, GAME_Y + y * BLOCK_SIZE + 5, BLOCK_SIZE - 12, BLOCK_SIZE - 12))


# 检查方块是否可以放在当前位置的函数
def valid_space(shape, position):
    for pos in convert_shape_format(shape, position):
        if pos[1] >= GAME_HEIGHT // BLOCK_SIZE or pos[1] < 0:
            print("Invalid: position out of vertical bounds", pos)
            return False
        if pos[0] < 0 or pos[0] > GAME_WIDTH // BLOCK_SIZE - 1:
            print("Invalid: position out of horizontal bounds", pos)
            return False
        if grid[pos[1]][pos[0]] != 0:
            print("Invalid: position occupied", pos)
            return False
    return True


def convert_shape_format(shape, position):
    positions = []
    shape_format = shape
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 1:
                # 计算每个方块的实际位置
                positions.append((position[0] + j, position[1] + i))
    return positions


# 在方块到达底部或碰到其他方块时固定它的位置的函数
def fix_shape():
    global grid, current_shape, current_position, next_shape
    formatted_shape = convert_shape_format(current_shape, current_position)
    for pos in formatted_shape:
        p_x, p_y = pos
        if p_y > -1:
            grid[p_y][p_x] = 1
    current_shape = next_shape  # 更新当前形状为下一个形状
    next_shape = random.choice(SHAPES)  # 生成新的下一个形状
    current_position = [GAME_WIDTH // BLOCK_SIZE // 2, 0]
    print("Shape fixed at position:", current_position)


# 检测和消除满行的函数
def check_lines():
    global grid, score, total_lines_removed
    lines_to_remove = []

    # 找出所有需要消除的行
    for i in range(len(grid)):
        if 0 not in grid[i]:
            lines_to_remove.append(i)

    # 如果有行需要消除，则执行闪烁动画
    if lines_to_remove:
        print("Playing line clear sound")  # 调试语句
        line_clear_sound.play()
        flash_lines_animation(screen, grid, lines_to_remove, WHITE, BLACK, BLOCK_SIZE, GAME_X, GAME_Y)

    # 删除行并更新得分
    lines_removed = len(lines_to_remove)
    for i in lines_to_remove:
        del grid[i]
        grid.insert(0, [0 for _ in range(GAME_WIDTH // BLOCK_SIZE)])

    if lines_removed > 0:
        base_score = lines_removed * 10
        bonus_score = (lines_removed - 1) * 10
        score += base_score + bonus_score
        total_lines_removed += lines_removed
        print("Lines removed:", lines_removed, "Total score:", score)


# 闪烁效果的函数
# 闪烁多行效果的函数
def flash_lines_animation(screen, grid, lines, color_flash, color_original, block_size, game_x, game_y, flash_times=2,
                          flash_duration=100):
    for _ in range(flash_times):
        # 为所有需要闪烁的行绘制闪烁色
        for y in lines:
            for x in range(len(grid[0])):
                pygame.draw.rect(screen, color_flash,
                                 (game_x + x * block_size, game_y + y * block_size, block_size, block_size))
        pygame.display.update()
        pygame.time.delay(flash_duration)
        # 还原所有需要闪烁的行的原色
        for y in lines:
            for x in range(len(grid[0])):
                pygame.draw.rect(screen, color_original,
                                 (game_x + x * block_size, game_y + y * block_size, block_size, block_size))
        pygame.display.update()
        pygame.time.delay(flash_duration)


# 游戏循环
running = True
move_time = 0  # 添加一个变量用于控制持续移动的速度
move_interval = 100  # 持续移动的时间间隔，单位毫秒

# 游戏初始化部分
# 当前方块的位置和形状
current_shape = random.choice(SHAPES)  # 初始化当前方块形状
next_shape = random.choice(SHAPES)  # 初始化下一个方块形状
current_position = [GAME_WIDTH // BLOCK_SIZE // 2, 0]
# 初始化得分
score = 0

# 方块下落的时间控制
fall_time = 0
fall_speed = 800  # 方块下落的速度，单位是毫秒
fall_speed_accelerated = 50  # 加速下落的速度

# 计算当前等级和下落速度
# 方块下落的基础速度和加速因子
base_fall_speed = 1000  # 基础速度为1000毫秒
fall_speed_acceleration_factor = 20  # 每级加速100毫秒


# 计算当前等级和下落速度的函数
def calculate_level_and_fall_speed(score):
    level = score // 100 + 1  # 每20分增加一个等级
    fall_speed = base_fall_speed - (level - 1) * fall_speed_acceleration_factor
    return level, max(fall_speed, 20)  # 防止速度过快


# 展示游戏开始
def show_start_screen():
    # 播放游戏主界面音乐
    Title_sound.play(-1)

    start_font = pygame.font.Font(font_path, 48)
    prompt_font = pygame.font.Font(font_path, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    Title_sound.stop()
                    Playing_sound.play(-1)
                    return  # 开始游戏

        screen.fill(BLACK)

        # 显示游戏标题
        title_text = start_font.render("TETRIS", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # 显示开始提示
        prompt_text = prompt_font.render("Press Enter to Start", True, WHITE)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()
        pygame.time.wait(100)


# 展示游戏结束
def show_game_over_screen(score):
    Title_sound.stop()
    # 播放游戏音乐
    Playing_sound.stop()
    # 播放游戏结束音乐
    GameOver_sound.play()

    game_over_font = pygame.font.Font(font_path, 48)
    SCORE_font = pygame.font.Font(font_path, 35)
    restart_font = pygame.font.Font(font_path, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    GameOver_sound.stop()
                    Playing_sound.play(-1)
                    return  # 重新开始游戏

        screen.fill(BLACK)

        # 显示游戏结束消息
        game_over_text = game_over_font.render("GAME OVER!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # 显示得分
        score_text = SCORE_font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # 显示重新开始指示
        restart_text = restart_font.render("Press [Enter] to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()
        pygame.time.wait(100)


# 初始化游戏主界面
show_start_screen()

# 进入游戏后
while running:
    # 在每个循环的开始更新形状
    if current_shape is None:
        current_shape = next_shape
        next_shape = random.choice(SHAPES)
        current_position = [GAME_WIDTH // BLOCK_SIZE // 2, 0]
    # 获取当前时间
    current_time = pygame.time.get_ticks()
    # 检查是否按下了下键
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        fall_speed_current = fall_speed_accelerated
    else:
        fall_speed_current = fall_speed

    # 检查是否持续按下左右键
    if current_time - move_time > move_interval:
        if keys[pygame.K_LEFT]:
            new_position = [current_position[0] - 1, current_position[1]]
            if valid_space(current_shape, new_position):
                current_position = new_position
        elif keys[pygame.K_RIGHT]:
            new_position = [current_position[0] + 1, current_position[1]]
            if valid_space(current_shape, new_position):
                current_position = new_position
        move_time = current_time

    # 游戏循环中添加键盘事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 加速下落
            if event.key == pygame.K_DOWN:
                new_position = [current_position[0], current_position[1] + 1]
                if valid_space(current_shape, new_position):
                    current_position = new_position
            # 旋转
            elif event.key == pygame.K_UP:
                # 调用旋转函数
                rotated_shape, new_position = rotate(current_shape, current_position)
                if valid_space(rotated_shape, new_position):
                    current_shape = rotated_shape
                    current_position = new_position

    # 方块自动下落逻辑
    if current_time - fall_time > fall_speed_current:
        fall_time = current_time
        new_position = [current_position[0], current_position[1] + 1]
        if valid_space(current_shape, new_position):
            current_position = new_position  # 方块下移一格
        else:
            fix_shape()  # 固定方块位置
            check_lines()  # 检查是否有满行
            # current_shape = random.choice(SHAPES)  # 生成新方块
            # current_position = [GAME_WIDTH // BLOCK_SIZE // 2, 0]

    # 下落速度随等级增加逻辑
    level, fall_speed = calculate_level_and_fall_speed(score)

    # 渲染逻辑
    screen.fill(LIGHT_GREY)
    pygame.draw.rect(screen, LIGHT_GREY, (GAME_X, GAME_Y, GAME_WIDTH, GAME_HEIGHT))

    # 渲染当前下落的方块
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                draw_block(current_position[0] + x, current_position[1] + y, BLACK)
    # 渲染游戏区域中的方块
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x, y, BLACK)

    # 绘制基本信息区域的背景
    pygame.draw.rect(screen, BLACK, (info_area_x, info_area_y, info_area_width, info_area_height))
    # 显示分数的灰色背景框
    pygame.draw.rect(screen, info_box_color1,
                     (score_box_x, score_box_y, score_box_width, score_box_height), border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color2,
                     (score_box_x + 2, score_box_y + 2, score_box_width - 5, score_box_height - 5),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color3,
                     (score_box_x + 5, score_box_y + 5, score_box_width - 10, score_box_height - 10),
                     border_radius=corner_radius)

    # 渲染“SCORE”标题文本
    score_title_text = font.render('SCORE', True, BLACK)
    # blit标题到屏幕，根据需要调整位置
    screen.blit(score_title_text, (score_box_x + padding, score_box_y + padding))
    # 渲染分数值
    score_value_text = font.render(str(score), True, BLACK)
    # blit分数值到屏幕，标题下方
    screen.blit(score_value_text,
                (score_box_x + padding + 70, score_box_y + score_title_text.get_height() + padding + 8))

    # 显示等级的灰色背景框及边框
    pygame.draw.rect(screen, info_box_color1,
                     (score_box_x, level_box_y, score_box_width, score_box_height), border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color2,
                     (score_box_x + 2, level_box_y + 2, score_box_width - 5, score_box_height - 5),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color3,
                     (score_box_x + 5, level_box_y + 5, score_box_width - 10, score_box_height - 10),
                     border_radius=corner_radius)
    # 渲染等级的标题文本
    level_title_text = font.render('LEVEL', True, BLACK)
    screen.blit(level_title_text, (score_box_x + padding, level_box_y + padding))
    # 渲染等级值
    level_value_text = font.render(str(level), True, BLACK)
    screen.blit(level_value_text,
                (score_box_x + padding + 70, level_box_y + level_title_text.get_height() + padding + 8))
    # 显示消除行数的灰色背景框及边框
    pygame.draw.rect(screen, info_box_color1,
                     (score_box_x, lines_box_y, score_box_width, score_box_height), border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color2,
                     (score_box_x + 2, lines_box_y + 2, score_box_width - 5, score_box_height - 5),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color3,
                     (score_box_x + 5, lines_box_y + 5, score_box_width - 10, score_box_height - 10),
                     border_radius=corner_radius)
    # 渲染消除行数
    lines_title_text = font.render('LINES', True, BLACK)
    screen.blit(lines_title_text, (score_box_x + padding, lines_box_y + padding))
    # 渲染消除行数值
    lines_value_text = font.render(str(total_lines_removed), True, BLACK)
    screen.blit(lines_value_text,
                (score_box_x + padding + 70, lines_box_y + lines_title_text.get_height() + padding + 8))
    # 显示下一个形状的灰色背景框及边框
    pygame.draw.rect(screen, info_box_color1,
                     (score_box_x, next_shape_box_y, score_box_width, next_shape_box_height),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color2,
                     (score_box_x + 2, next_shape_box_y + 2, score_box_width - 5, next_shape_box_height - 5),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, info_box_color3,
                     (score_box_x + 5, next_shape_box_y + 5, score_box_width - 10, next_shape_box_height - 10),
                     border_radius=corner_radius)

    # 渲染下一个方块
    display_next_shape(next_shape, screen)  # 假设 next_shape 是下一个方块的形状
    # 渲染分界线的逻辑
    border_x = GAME_X + GAME_WIDTH  # 分界线的x坐标
    pygame.draw.line(screen, BORDER_COLOR, (border_x, 0), (border_x, SCREEN_HEIGHT), BORDER_WIDTH)

    # 更新显示
    pygame.display.flip()

    # 游戏结束的检查
    if game_over():
        show_game_over_screen(score)
        # 重新初始化游戏状态
        grid = [[0 for _ in range(GAME_WIDTH // BLOCK_SIZE)] for _ in range(GAME_HEIGHT // BLOCK_SIZE)]
        score = 0
        total_lines_removed = 0
        current_shape = random.choice(SHAPES)
        next_shape = random.choice(SHAPES)
        current_position = [GAME_WIDTH // BLOCK_SIZE // 2, 0]
        running = True

# 退出pygame
pygame.quit()