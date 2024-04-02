import json
import random
import pygame
from math import sqrt


class Star:
    def __init__(self):
        self.p_x = 0
        self.p_y = 0
        self.v_x = 0
        self.v_y = 0
        self.m = 0
        self.mv = 0
        self.f_x = 0
        self.f_y = 0
        self.pg = None

    def move(self, t=0.01, max_x=None, max_y=None, collapse=False):
        if collapse:
            self.p_x += (964 - self.p_x) * 0.01
            self.p_y += (500 - self.p_y) * 0.01
        else:
            if self.m > 0:
                self.p_x += (self.v_x * t) + 0.5 * (self.f_x / self.m) * t * t
                self.p_y += (self.v_y * t) + 0.5 * (self.f_y / self.m) * t * t
                if max_x is not None and (self.p_x < 0 or self.p_x > max_x):
                    self.v_x = -1 * self.v_x
                    self.p_x = 0
                else:
                    self.v_x += (self.f_x / self.m) * t
                if max_y is not None and (self.p_y < 0 or self.p_y > max_y):
                    self.v_y = -1 * self.v_y
                    self.p_y = 0
                else:
                    self.v_y += (self.f_y / self.m) * t
                self.mv = self.m * sqrt((self.v_x * self.v_x) + (self.v_y * self.v_y))


class Space:
    def __init__(self, screen_x, screen_y):
        self.star_list = []
        self.G = 100  # 节目效果
        self.s_x = screen_x
        self.s_y = screen_y
        self.max_id = 0
        self.parm = 0
        self.color = ['pink', 'yellow', 'lightblue', 'white', 'green']

    def load_space(self, path):
        with open(path,'r', encoding='utf-8') as f:
            space_json = json.load(f)
        for sid, st in space_json.items():
            self.add_star(m=st['m'], px=st['px'], py=st['py'], vx=st['vx'], vy=st['vy'])

    def save_space(self, path):
        space_json = {}
        for st in self.star_list:
            star = st['star']
            sid = st['id']
            space_json[sid] = {'m':star.m, 'px':star.p_x,'py':star.p_y,'vx':star.v_x,'vy':star.v_y}
        with open(path,'w', encoding='utf-8') as f:
            json.dump(space_json,f)



    def add_star(self, m=None, px=None, py=None, vx=None, vy=None):
        """
        创建星球. 不带参数时属性随机
        """
        star = Star()
        star.m = m if m is not None else random.randrange(300, 500)
        star.p_x = px if px is not None else random.randrange(round(0.1 * self.s_x, 0), round(0.9 * self.s_x, 0))
        star.p_y = py if py is not None else random.randrange(round(0.1 * self.s_y, 0), round(0.9 * self.s_y, 0))
        star.v_x = vx if vx is not None else random.randrange(-60, 60)
        star.v_y = vy if vy is not None else random.randrange(-60, 60)
        star.pg = pygame.Vector2(star.p_x, star.p_y)
        sid = self.max_id + 1
        color = self.color[random.randrange(0, 4)]
        self.star_list.append({'id': sid, 'star': star, 'color': color})
        self.max_id += 2

    def destory_star(self, px, py):
        """
        摧毁星球
        """
        destory_id = []
        for star_info in self.star_list:
            star = star_info['star']
            sid = star_info['id']
            if abs(star.p_x - px) <= 15 and abs(star.p_y - py) <= 15:
                destory_id.append(sid)
        self.star_list = [x for x in self.star_list if x['id'] not in destory_id]

    def get_f(self, star1, star2):
        """
        计算star2 对 star1 的力
        牛顿
        """
        distance_2 = ((star1.p_x - star2.p_x) * (star1.p_x - star2.p_x)) + ((star1.p_y - star2.p_y) * (star1.p_y - star2.p_y))
        f = 0 if distance_2 < 4 else (self.G * star1.m * star2.m) / distance_2
        f_x = 0 if distance_2 < 4 else f * (star2.p_x - star1.p_x) / sqrt(distance_2)
        f_y = 0 if distance_2 < 4 else f * (star2.p_y - star1.p_y) / sqrt(distance_2)
        return f_x, f_y

    def run(self, limit=False, collapse=False):
        """
        宇宙运行
        1. 计算每个星球受到的合力, 分解到 x,y方向
        2. 根据受力移动星球位置
        """
        destory_id = []  # 每次循环需要摧毁的星球
        for st in self.star_list:
            star = st['star']
            pid = st['id']
            fx = 0  # x方向合力
            fy = 0  # y方向合力
            for sub_st in self.star_list:
                sub_pid = sub_st['id']
                sub_star = sub_st['star']
                max_r = max((self.parm * star.m), (self.parm * sub_star.m))  # 洛希极限(魔改版)
                if pid == sub_pid or pid in destory_id or sub_pid in destory_id:
                    continue
                # 两颗星球距离小于洛希极限
                # 按动量守恒合并星球
                if abs(star.p_x - sub_star.p_x) <= max_r and abs(star.p_y - sub_star.p_y) <= max_r:
                    star.v_x = ((star.v_x * star.m) + (sub_star.v_x * sub_star.m)) / (star.m + sub_star.m)
                    star.v_y = ((star.v_y * star.m) + (sub_star.v_y * sub_star.m)) / (star.m + sub_star.m)
                    star.m = star.m + sub_star.m
                    destory_id.append(sub_pid)
                    continue
                sub_fx, sub_fy = self.get_f(star, sub_star)
                fx += sub_fx
                fy += sub_fy
            star.f_x = fx
            star.f_y = fy

        # 更新每颗星球位置
        for st in self.star_list:
            star = st['star']
            if limit:
                star.move(max_x=self.s_x, max_y=self.s_y, collapse=collapse)
            else:
                star.move(collapse=collapse)
        self.star_list = [x for x in self.star_list if x['id'] not in destory_id]

    def fix_view(self, flag):
        """
        调整视野
        默认将宇宙质心作为窗口中心
        """
        d_x = 0  # 偏移距离
        d_y = 0
        if flag == 'w':
            d_y = 0.8 * self.s_y
        elif flag == 'a':
            d_x = 0.8 * self.s_x
        elif flag == 's':
            d_y = -0.8 * self.s_y
        elif flag == 'd':
            d_x = -0.8 * self.s_x
        elif flag == 'r':
            x = 0
            y = 0
            total_x = 0
            total_y = 0
            for st in self.star_list:
                p = st['star']
                x += p.p_x * p.m
                y += p.p_y * p.m
                total_x += p.m
                total_y += p.m
            x_mean = x / total_x
            y_mean = y / total_y
            d_x = (0.5 * self.s_x) - x_mean
            d_y = (0.5 * self.s_y) - y_mean
        else:
            return None

        for star_info in self.star_list:
            star = star_info['star']
            star.p_x += d_x * 0.01

        for star_info in self.star_list:
            star = star_info['star']
            star.p_y += d_y * 0.01

    def get_info_summary(self):
        info_list = ['Total: ' + str(len(self.star_list)), '|   m   | (   vx   ,  vy   )  |  (   px , py   ) |']
        for st in self.star_list:
            p = st['star']
            tmp = '| ' + str(round(p.m)) + ' '
            tmp += '| ( ' + str(round(p.v_x)) + ' , ' + str(round(p.v_y)) + ') '
            tmp += '| ( ' + str(round(p.p_x)) + ' , ' + str(round(p.p_y)) + ') '
            info_list.append(tmp)
        return info_list
