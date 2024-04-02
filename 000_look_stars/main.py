import sys

import pygame
from rule import Space

# 窗口大小
screen_x = 1920
screen_y = 1080
fullscreen = True

# 初始星球数
N_STARS = 5

# 初始化
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

# 创建宇宙
space = Space(screen_x, screen_y)

# # 手动创建星球
# space.add_star(m=600,px=100)
# space.add_star(m=600)

# 随机创建星球
for _ in range(0, N_STARS):
    space.add_star()


# space.load_space('100.json')
# space.save_space('2.json')

m_total = 0
for star_info in space.star_list:
    star = star_info['star']
    m_total += star.m
space.parm = 2 * N_STARS / m_total

view_auto = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    collapse = False  # 宇宙坍缩
    view_flag = 'r'  # 自动移动视野
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()
    elif pygame.key.get_pressed()[pygame.K_f]:
        if fullscreen:
            screen = pygame.display.set_mode((screen_x, screen_y))
            fullscreen = False
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            fullscreen = True
    elif pygame.key.get_pressed()[pygame.K_SPACE]:
        collapse = True
    elif pygame.key.get_pressed()[pygame.K_w]:
        view_flag = 'w'
        view_auto = False
    elif pygame.key.get_pressed()[pygame.K_a]:
        view_flag = 'a'
        view_auto = False
    elif pygame.key.get_pressed()[pygame.K_s]:
        view_flag = 's'
        view_auto = False
    elif pygame.key.get_pressed()[pygame.K_d]:
        view_flag = 'd'
        view_auto = False
    elif pygame.key.get_pressed()[pygame.K_r]:
        view_flag = 'r'
        view_auto = True
    elif pygame.mouse.get_pressed():
        ml, mm, mr = pygame.mouse.get_pressed()
        px, py = pygame.mouse.get_pos()
        if ml:
            space.add_star(m=150, vx=0, vy=0, px=px, py=py)
        elif mr:
            space.destory_star(px=px, py=py)

    # 宇宙运行
    space.run(collapse=collapse)
    if view_auto is True:
        space.fix_view(flag='r')
    elif view_auto is False and view_flag == 'r':
        space.fix_view(flag=None)
    else:
        space.fix_view(flag=view_flag)

    # 黑色背景
    screen.fill("black")

    # 绘制每颗星球
    for star_info in space.star_list:
        star = star_info['star']
        color = star_info['color']
        pygame.draw.circle(screen, color, star.pg, round(star.m * space.parm))
        star.pg.x = star.p_x
        star.pg.y = star.p_y

    # 概况信息
    info_list = space.get_info_summary()
    pi = 10
    for info in info_list:
        font = pygame.font.SysFont("Arial", 16)
        txt = font.render(info, True, (255, 255, 255))
        screen.blit(txt, (10, pi))
        pi += 15

    pygame.display.flip()
    dt = clock.tick(1000)
