import sys
import pygame


import sudokum

input_sudo = sudokum.generate(mask_rate=0.7)

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

color = {
    'bg':'Honeydew',
    'line':'Black',
    'msg':'Black',
    'cell_bg': 'Wheat',
    'cell_font': 'DarkGreen',
    'selected_cell_bg': 'DarkGreen',
    'selected_cell_font': 'Wheat',
    'draft_bg': 'Wheat',
    'draft_font':'SlateGray',
    'selected_draft_bg': 'SlateGray',
    'selected_draft_font':'Wheat',
}




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
    """
    每次调用只做一个步骤
    """
    # 清理行: 从每行列块草稿里清除已确定的值
    for n in range(1, 10):
        vr = bd[str(ii) + str(n)]
        if len(vr) > 1 and value in vr:
            bd[str(ii) + str(n)] = [x for x in vr if x != value]
            return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(ii), str(n)), ii, n

        vc = bd[str(n) + str(jj)]
        if len(vc) > 1 and value in vc:
            bd[str(n) + str(jj)] = [x for x in vc if x != value]
            return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(n), str(jj)), n, jj
    for bi in range(int(ii / 3.5) * 3 + 1, int(ii / 3.5) * 3 + 4):
        for bj in range(int(jj / 3.5) * 3 + 1, int(jj / 3.5) * 3 + 4):
            vb = bd[str(bi) + str(bj)]
            if len(vb) > 1 and value in vb:
                bd[str(bi) + str(bj)] = [x for x in vb if x != value]
                return bd, 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(bi), str(bj)), bi, bj
    return 'Done', 'Done', 0, 0


def shoot_2():
    pass


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

    screen.fill(color['bg'])

    # 画格子
    g_size = 72
    g_margin = 8
    for i in range(1,11):
        line_width = 5 if i in [1,4,7,10] else 1
        pygame.draw.line(screen, color['line'], (i*g_size-g_margin, g_size-g_margin), (i*g_size-g_margin, g_size*10-g_margin),line_width)  
        pygame.draw.line(screen, color['line'], (g_size-g_margin,i*g_size-g_margin), (g_size*10-g_margin,i*g_size-g_margin),line_width)  

    cell_margin = 30
    for i in range(1, 10):
        for j in range(1, 10):
            v = board[str(i) + str(j)]
            if len(v) == 1:
                cell_radius = 30
                if i == data[0] and j == data[1]:
                    font_color = color['selected_cell_font']
                    cell_color = color['selected_cell_bg']
                else:
                    font_color = color['cell_font']
                    cell_color = color['cell_bg']
                cell = (j * g_size + cell_margin, i * g_size + cell_margin)
                number_font = pygame.font.SysFont("Arial", 20)
                number_text = number_font.render(str(v[0]), True, font_color)
                number_rect = number_text.get_rect(center=cell)
                pygame.draw.circle(screen, cell_color, cell, cell_radius)
                screen.blit(number_text, number_rect)  # 在指定位置绘制文字
            else:
                cell_radius = 10
                if i == data[2] and j == data[3]:
                    font_color = color['selected_draft_font']
                    cell_color = color['selected_draft_bg']
                else:
                    font_color = color['draft_font']
                    cell_color = color['draft_bg']
                for vv in v:
                    cell = (j * g_size + get_vp('x', vv), i * g_size + get_vp('y', vv))
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
        txt = font.render(info, True, color['msg'])
        screen.blit(txt, (800, pi))
        pi += 15
    pygame.display.flip()
    dt = clock.tick(30)
