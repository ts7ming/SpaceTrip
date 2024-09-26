import sys
import time
import random
import pygame


def is_safe(board, row, col, num):
    # 检查行
    for x in range(9):
        if board[row][x] == num:
            return False

            # 检查列
    for x in range(9):
        if board[x][col] == num:
            return False

            # 检查3x3的格子
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


input_sudo = [[0] * 9 for _ in range(9)]
# 随机填充一些数字以开始解决过程
for _ in range(80):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    num = random.randint(1, 9)
    if is_safe(input_sudo, row, col, num):
        input_sudo[row][col] = num

# input_sudo = [
#     [0, 9, 7, 3, 6, 0, 4, 8, 5],
#     [1, 4, 8, 5, 2, 3, 9, 7, 0],
#     [5, 0, 1, 7, 9, 4, 3, 2, 8],
#     [6, 8, 9, 0, 7, 2, 5, 3, 0],
#     [3, 2, 0, 8, 0, 9, 7, 6, 1],
#     [7, 5, 4, 2, 1, 6, 8, 9, 3],
#     [9, 7, 6, 4, 8, 0, 2, 1, 3],
#     [4, 0, 3, 6, 0, 8, 9, 4, 7],
#     [8, 3, 2, 9, 7, 4, 1, 5, 0]
# ]

screen_x = 1000
screen_y = 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()


def get_vp(xy, value):
    if xy == 'x':
        if value in [1, 4, 7]:
            vp = 10
        elif value in [2, 5, 8]:
            vp = 30
        else:
            vp = 50
    else:
        if value in [1, 2, 3]:
            vp = 10
        elif value in [4, 5, 6]:
            vp = 30
        else:
            vp = 50
    return vp


def shoot(bd, ii, jj, value):
    for n in range(1, 10):
        # 清理行
        vr = bd[str(ii) + str(n)]
        if len(vr) > 1 and value in vr:
            bd[str(ii) + str(n)] = [x for x in vr if x != value]
            return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(ii), str(n)), ii, n
        # 清理列
        vc = bd[str(n) + str(jj)]
        if len(vc) > 1 and value in vc:
            bd[str(n) + str(jj)] = [x for x in vc if x != value]
            return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(n), str(jj)), n, jj
    # 清理块
    for bi in range(int(ii / 3.5) * 3 + 1, int(ii / 3.5) * 3 + 4):
        for bj in range(int(jj / 3.5) * 3 + 1, int(jj / 3.5) * 3 + 4):
            vb = bd[str(bi) + str(bj)]
            if len(vb) > 1 and value in vb:
                bd[str(bi) + str(bj)] = [x for x in vb if x != value]
                return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(bi), str(bj)), bi, bj
    return 'Done', 'Done', 0, 0


def update(bd):
    for ii in range(1, 10):
        for jj in range(1, 10):
            values = bd[str(ii) + str(jj)]
            if len(values) == 1:
                status, shoot_msg, rn, cn = shoot(bd, ii, jj, values[0])
                if shoot_msg == 'Done':
                    continue
                data = [ii, jj, rn, cn]
                return bd, shoot_msg, data
    return bd, 'Done', [0, 0, 0, 0]


board = {}
for i in range(1, 10):
    for j in range(1, 10):
        if input_sudo[i - 1][j - 1] == 0:
            board[str(i) + str(j)] = [x for x in range(1, 10)]
        else:
            board[str(i) + str(j)] = [input_sudo[i - 1][j - 1]]
count = 0
msg = ''
data = [0, 0, 0, 0]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()
    elif pygame.mouse.get_pressed() and msg != 'Done':
        ml, mm, mr = pygame.mouse.get_pressed()
        px, py = pygame.mouse.get_pos()
        if ml:
            count += 1
            board, msg, data = update(board)
    else:
        pass

    screen.fill("black")
    for i in range(1, 10):
        for j in range(1, 10):
            v = board[str(i) + str(j)]
            if len(v) == 1:
                cell_radius = 30
                if i == data[0] and j == data[1]:
                    font_color = 'white'
                    cell_color = 'green'
                else:
                    font_color = 'blue'
                    cell_color = 'white'
                cell = (j * 70 + 30, i * 70 + 30)
                number_font = pygame.font.SysFont("Arial", 20)
                number_text = number_font.render(str(v[0]), True, font_color)
                number_rect = number_text.get_rect(center=cell)
                pygame.draw.circle(screen, cell_color, cell, cell_radius)
                screen.blit(number_text, number_rect)  # 在指定位置绘制文字
            else:
                cell_radius = 10
                if i == data[2] and j == data[3]:
                    font_color = 'white'
                    cell_color = 'green'
                else:
                    font_color = 'red'
                    cell_color = 'white'
                for vv in v:
                    cell = (j * 70 + get_vp('x', vv), i * 70 + get_vp('y', vv))
                    number_font = pygame.font.SysFont("Arial", 15)
                    number_text = number_font.render(str(vv), True, font_color)
                    number_rect = number_text.get_rect(center=cell)
                    pygame.draw.circle(screen, cell_color, cell, cell_radius)
                    screen.blit(number_text, number_rect)  # 在指定位置绘制文字

    # 概况信息

    info_list = ['step:  ' + str(count), '', msg]
    pi = 80
    for info in info_list:
        font = pygame.font.SysFont("Arial", 16)
        txt = font.render(info, True, (255, 255, 255))
        screen.blit(txt, (800, pi))
        pi += 15
    pygame.display.flip()
    dt = clock.tick(30)
