import sys
import pygame
import sudokum
from sudoku_lib import Button

input_sudo = sudokum.generate(mask_rate=0.4)

input_sudo = [
    [0, 0, 0, 0, 8, 0, 5, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 1, 7],
    [0, 5, 0, 4, 1, 0, 0, 0, 0],
    [0, 9, 0, 7, 0, 1, 0, 0, 0],
    [0, 4, 1, 5, 0, 0, 0, 0, 2],
    [0, 0, 6, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 3, 0, 5, 9, 0, 0],
    [0, 3, 0, 0, 0, 0, 6, 2, 0],
    [0, 2, 0, 0, 0, 6, 0, 0, 0]
]

# input_sudo = [
#     [3, 5, 7, 0, 4, 2, 1, 0, 0],
# [1, 0, 0, 5, 0, 0, 0, 0, 7],
# [8, 0, 4, 0, 7, 1, 2, 0, 3],
# [6, 3, 0, 7, 0, 4, 8, 2, 1],
# [9, 0, 0, 2, 0, 8, 0, 0, 4],
# [2, 4, 0, 1, 5, 6, 7, 0, 0],
# [4, 6, 9, 8, 2, 0, 3, 1, 0],
# [5, 0, 3, 0, 1, 9, 6, 0, 2],
# [7, 0, 2, 0, 6, 0, 0, 0, 8],
# ]

for x in input_sudo:
    print(x,',')

pos = {
    'board': (50,50),
    'ctrl': (750, 50),
    'msg': (850, 50),
}

size = {
    'grid': 72,
    'grid_line': 5,
    'grid_line_light':1,
    'grid_margin':6,
    'cell_margin':30,
    'cell_radius_cfm':28,
    'cell_radius_draft':13,
    'font_cfm':23,
    'font_draft':15
}

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
    从每行列块草稿里清除已确定的值
    每次调用只做一个步骤
    """
    for n in range(1, 10):
        # 行
        vr = bd[str(ii) + str(n)]
        if len(vr) > 1 and value in vr:
            bd[str(ii) + str(n)] = [x for x in vr if x != value]
            return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(ii), str(n)), ii, n
        # 列
        vc = bd[str(n) + str(jj)]
        if len(vc) > 1 and value in vc:
            bd[str(n) + str(jj)] = [x for x in vc if x != value]
            return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(n), str(jj)), n, jj
    # 块
    for bi in range(int(ii / 3.5) * 3 + 1, int(ii / 3.5) * 3 + 4):
        for bj in range(int(jj / 3.5) * 3 + 1, int(jj / 3.5) * 3 + 4):
            vb = bd[str(bi) + str(bj)]
            if len(vb) > 1 and value in vb:
                bd[str(bi) + str(bj)] = [x for x in vb if x != value]
                return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(bi), str(bj)), bi, bj
    return 'Done', 0, 0


def search(bd):
    """
    从每行列块草稿里找到只出现一次的值, 更新为确定值
    每次调用只做一个步骤
    """
    for n in range(1, 10):
        # 行
        cfm_v = []
        for ii in range(1,10): # 遍历cell
            bdv = bd[str(n)+str(ii)]
            if len(bdv)==1:
                cfm_v.append(bdv[0])
        v_cnt = {}
        v_cnt_inx = {}
        for v in range(1,10):
            if v in cfm_v: continue
            if v not in v_cnt.keys():
                v_cnt[v] = 0
                v_cnt_inx[v]=0
            for ii in range(1,10):
                bdv = bd[str(n)+str(ii)]
                if v in bdv:
                    v_cnt[v]+=1
                    v_cnt_inx[v] = ii
        for v in range(1, 10):
            if v in cfm_v: continue
            if v_cnt[v] == 1:
                bd[str(n)+str(v_cnt_inx[v])] = [v]
                return 'Rise value:[ %s ] in cell(%s, %s)' % (str(v), str(n), str(v_cnt_inx[v])), n, v_cnt_inx[v]
        # 列
        cfm_v = []
        for ii in range(1,10):
            bdv = bd[str(ii)+str(n)]
            if len(bdv)==1:
                cfm_v.append(bdv[0])
        v_cnt = {}
        v_cnt_inx = {}
        for v in range(1,10):
            if v in cfm_v: continue
            if v not in v_cnt.keys():
                v_cnt[v] = 0
                v_cnt_inx[v]=0
            for ii in range(1,10):
                bdv = bd[str(ii)+str(n)]
                if v in bdv:
                    v_cnt[v]+=1
                    v_cnt_inx[v] = ii
        for v in range(1, 10):
            if v in cfm_v: continue
            if v_cnt[v] == 1:
                bd[str(v_cnt_inx[v])+str(n)] = [v]
                return 'Rise value:[ %s ] in cell(%s, %s)' % (str(v), str(n), str(v_cnt_inx[v])), n, v_cnt_inx[v]
            

    return 'Done', 0, 0


def update(bd):
    for ii in range(1, 10):
        for jj in range(1, 10):
            values = bd[str(ii) + str(jj)]
            if len(values) == 1:
                shoot_msg, rn, cn = shoot(bd, ii, jj, values[0])
                if shoot_msg == 'Done':
                    continue
                data = [ii, jj, rn, cn]
                return shoot_msg, data

    search_msg, rn, cn = search(bd)
    if search_msg == 'Done':
        return 'Done', [0, 0, 0, 0]
    else:
        data = [0, 0, rn, cn]
        return search_msg, data


screen_x = 1200
screen_y = 800


pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

button_go = Button(750,50,80,50,'Go','SteelBlue')
button_draft = Button(750,110,80,50,'AutoGo','SteelBlue')


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
msg_display = []
auto = False
todo = True
while True:
    go = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif button_draft.is_clicked(event):
            auto = True if auto is False else False
            button_draft.color = 'Lime' if button_draft.color=='SteelBlue' else 'SteelBlue'
            break
        elif button_go.is_clicked(event):
            go = True
            button_go.color = 'Lime'
            break
        else:
            pass

    if todo and (auto or go):
        msg, data = update(board)
        count += 1
        if msg not in msg_display:
            msg_display.append(msg)
            if len(msg_display)>40:
                msg_display.pop(0)
        if msg == 'Done':
            todo = False

    screen.fill(color['bg'])
    button_go.draw(screen)
    button_draft.draw(screen)

    # 画格子
    g_size = size['grid']
    g_margin = size['grid_margin']
    for i in range(1,11):
        line_width = size['grid_line'] if i in [1,4,7,10] else size['grid_line_light']
        pygame.draw.line(screen, color['line'], (i*g_size-g_margin, g_size-g_margin), (i*g_size-g_margin, g_size*10-g_margin),line_width)  
        pygame.draw.line(screen, color['line'], (g_size-g_margin,i*g_size-g_margin), (g_size*10-g_margin,i*g_size-g_margin),line_width)  

    cell_margin = size['cell_margin']
    for i in range(1, 10):
        for j in range(1, 10):
            v = board[str(i) + str(j)]
            if len(v) == 1:
                if i == data[0] and j == data[1]:
                    font_color = color['selected_cell_font']
                    cell_color = color['selected_cell_bg']
                else:
                    font_color = color['cell_font']
                    cell_color = color['cell_bg']
                cell = (j * g_size + cell_margin, i * g_size + cell_margin)
                number_font = pygame.font.SysFont("Arial", size['font_cfm'])
                number_text = number_font.render(str(v[0]), True, font_color)
                number_rect = number_text.get_rect(center=cell)
                pygame.draw.circle(screen, cell_color, cell, size['cell_radius_cfm'])
                screen.blit(number_text, number_rect)  # 在指定位置绘制文字
            else:
                if i == data[2] and j == data[3]:
                    font_color = color['selected_draft_font']
                    cell_color = color['selected_draft_bg']
                else:
                    font_color = color['draft_font']
                    cell_color = color['draft_bg']
                for vv in v:
                    cell = (j * g_size + get_vp('x', vv), i * g_size + get_vp('y', vv))
                    number_font = pygame.font.SysFont("Arial", size['font_draft'])
                    number_text = number_font.render(str(vv), True, font_color)
                    number_rect = number_text.get_rect(center=cell)
                    pygame.draw.circle(screen, cell_color, cell, size['cell_radius_draft'])
                    screen.blit(number_text, number_rect)  # 在指定位置绘制文字

    # 概况信息
    info_list = ['step:  ' + str(count), ''] + msg_display
    pi = pos['msg'][1]
    for info in info_list:
        font = pygame.font.SysFont("Arial", size['cell_radius_draft'])
        txt = font.render(info, True, color['msg'])
        screen.blit(txt, (pos['msg'][0], pi))
        pi += 15
    pygame.display.flip()
    dt = clock.tick(30)
    button_go.color = 'SteelBlue'
