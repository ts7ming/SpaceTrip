import pygame
from random import choice, randint
from math import sqrt, pow


class Measure:
    def __init__(self, k=None, v=None):
        pass

    def set(self, k, v):
        pass


class Creature:
    def __init__(self, oid):
        self.oid = oid
        self.duration = 0
        self.running = None
        self.g_py = None
        self.g_px = None
        self.__i = {
            '位置$纵': randint(0, 100),
            '位置$横': randint(0, 100),
            '视野': 1000,  # 默认视野大小
            '攻击范围': 1,
            '防御力': 7,
            '攻击力': 10,
            '行动速度': 1,
            '攻击速度': 1,
            '生命值': 100
        }

    def game(self):
        self.g_px = self.v('位置$横') * 5
        self.g_py = self.v('位置$纵') * 5


    def v(self, addr: str, value=None):
        if addr in self.__i:
            if value is None:
                return self.__i[addr]
            else:
                self.__i[addr] = value
                return 'Done'
        else:
            return 'tmp'

    def move(self, dx, dy):
        self.__i['位置$横'] += dx
        self.__i['位置$纵'] += dy

    @staticmethod
    def __active(v=None):
        if v is None:
            v = randint(-1, 1)
        if v > 0.5:
            return 1
        elif v < -0.5:
            return -1
        else:
            return 0

    def wait(self):
        self.move(self.__active() * self.v('行动速度'), self.__active() * self.v('行动速度'))

    def move_to(self, tg_obj):
        if self.duration == 0:
            self.duration = 100
        dx = self.__active(tg_obj.v('位置$横') - self.v('位置$横')) * self.v('行动速度')
        dy = self.__active(tg_obj.v('位置$纵') - self.v('位置$纵')) * self.v('行动速度')
        self.move(dx, dy)
        self.duration -= 1

    def move_away(self, tg_obj):
        if self.duration == 0:
            self.duration = 100
        dx = -1 * self.__active(tg_obj.v('位置$横') - self.v('位置$横')) * self.v('行动速度')
        dy = -1 * self.__active(tg_obj.v('位置$纵') - self.v('位置$纵')) * self.v('行动速度')
        self.move(dx, dy)
        self.duration -= 1

    def distance(self, tg_obj):
        return round(sqrt(pow(self.v('位置$横') - tg_obj.v('位置$横'), 2) + pow(self.v('位置$纵') - tg_obj.v('位置$纵'), 2)), 4)

    def attack(self, tg_obj):
        tg_obj.v('生命值', tg_obj.v('生命值') - self.v('攻击力'))


class World:
    def __init__(self):
        self.__obj_id = 1
        self.objs = []

    def search(self, tg_obj):
        """
        搜索视野范围内距离最近的对象
        :param tg_obj:
        :return:
        """
        result_obj = None
        temp_dis = float('inf')
        for temp_obj in self.objs:
            if temp_obj.oid == tg_obj.oid:
                continue
            dis = tg_obj.distance(temp_obj)
            if dis <= tg_obj.v('视野') and dis < temp_dis:
                temp_dis = dis
                result_obj = tg_obj
        return result_obj

    def add_creature(self, i):
        tmp_c = Creature(self.__obj_id)
        for k, v in i.items():
            tmp_c.v(k, v)
        self.objs.append(tmp_c)
        self.__obj_id += 1

    def run(self):
        cnt = 1
        param = {}
        for obj in self.objs:
            info = str(cnt) + '号生物(攻%s防%s):' % (str(obj.v('攻击力')), str(obj.v('防御力')))
            if obj.duration > 0:
                obj.running(**param)
                continue
            param = {}
            tg_obj = self.search(obj)
            if tg_obj is None:
                obj.running = obj.move
                param = {'dx': randint(-1, 1), 'dy': randint(-1, 1)}
                print(info + '无所事事1')
            elif obj.v('攻击力') - tg_obj.v('防御力') > 0:
                dis = obj.distance(tg_obj)
                if dis <= obj.v('攻击范围'):
                    obj.running = obj.attack  # 攻击
                    param = {'tg_obj': tg_obj}
                    print(info + '攻击')
                else:
                    obj.running = obj.move_to  # 追击猎物
                    param = {'tg_obj': tg_obj}
                    print(info + '追击猎物')
            # elif tg_obj.v('攻击力') - obj.v('防御力') > 1:
            #     obj.running = obj.move_away  # 躲避强敌
            #     param = {'tg_obj': tg_obj}
            #     print(info + '躲避强敌')
            else:
                obj.running = obj.move  # 无所事事
                param = {'dx': randint(-1, 1), 'dy': randint(-1, 1)}
                print(info + '无所事事2')
            obj.running(**param)
            cnt += 1


screen_x = 1000
screen_y = 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption('Jungle')

w = World()
# for _ in range(0, 3):
#     w.add_creature()


w.add_creature({'攻击力': 20, '防御力': 9, '行动速度': 6})
w.add_creature({'攻击力': 7, '防御力': 9, '行动速度': 9})

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill('Honeydew')

    for t_obj in w.objs:
        t_obj.game()
        hp = round(t_obj.v('生命值')/10,0)
        pygame.draw.circle(screen, 'LawnGreen', (t_obj.g_px, t_obj.g_py), hp)

    w.run()

    pygame.display.flip()
    dt = clock.tick(60)
