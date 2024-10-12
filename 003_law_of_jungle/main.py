import pygame
from random import choice, randint



class Measure:
    def __init__(self, k=None, v=None):
        pass
    
    def set(self, k, v):
        pass


class Creature:
    def __init__(self):
        self.__i = {}

    def to_game(self):
        pass

    def __build(self):
        self.__i = {
            '位置': {'纵': randint(0,100), '横': randint(0,100)},
            '视野': 10, # 默认视野大小
            '攻击范围': 1,
            '防御力': 2,
            '行动速度': 1,
            '攻击速度': 1,
            '生命值': 100
        }

    def v(self, addr:str, value=None):
        addr_idx = addr.split('$')
        tmp = ''
        res = self.__i.copy()
        for a in addr_idx:
            tmp += a +'$'
            try:
                res = res[a]
            except:
                return 0, tmp
        if value is None:
            return 1, res
        else:
            run = 'self.__i[' + addr.replace('$','][') + ']=value'
            exec(run)
            return 1, 'Done'


    def soul(self, k=None, v=None):
        pass

    def __move(self, dx, dy):
        self.pos.update(self.pos.x + dx, self.pos.y + dy)

    def __active(self, v=None):
        if v is None:
            v = randint(-1,1)
        if v >0.5:
            return 1
        elif v<-0.5:
            return -1
        else:
            return 0

    def wait(self):
        self.__move(self.__active()*self.Spd, self.__active()*self.Spd)

    def move_to(self, p:Pos):
        dx =  self.__active(p.x-self.pos.x) * self.Spd
        dy =  self.__active(p.y-self.pos.y) * self.Spd
        self.__move(dx, dy)

    def move_away(self, p:Pos):
        dx =  -1 * self.__active(p.x-self.pos.x) * self.Spd
        dy =  -1 * self.__active(p.y-self.pos.y) * self.Spd
        self.__move(dx, dy)

    def attack(self, obj):
        pass


class World:
    map_size = {'x':500,'y':500}
    def __init__(self):
        self.objs = []

    def search(self, pos:Pos, distance):
        result_obj = None
        temp_dis2 = float('inf')
        for obj in self.objs:
            dis_x = abs(obj.pos.x - pos.x)
            dis_y = abs(obj.pos.y-pos.y)
            if dis_x <= distance and dis_y<=distance:
                new_dis2 = dis_x + dis_y
                if new_dis2 < temp_dis2:
                    temp_dis = new_dis2
                    result_obj = obj
        return result_obj

    def add_creature(self):
        self.objs.append(Creature())

    def run(self):
        cnt = 1
        for obj in self.objs:
            info = str(cnt)+'号生物(攻%s防%s):' % (str(obj.Atk), str(obj.Def))
            tg_obj = self.search(obj.pos, obj.search_distance)
            if tg_obj is None:
                # obj.wait() # 无所事事
                print(info+'无所事事')
            elif obj.Atk - tg_obj.Def > 3 and tg_obj.Atk - obj.Def<2:
                if abs(obj.pos.x - tg_obj.pos.x)<= obj.attack_distance and abs(obj.pos.y - tg_obj.pos.y)<= obj.attack_distance:
                    obj.attack(tg_obj) # 攻击
                    print(info+'攻击')
                else:
                    obj.move_to(p=tg_obj.pos) # 追击猎物
                    print(info+'追击猎物')
            elif tg_obj.Atk - obj.Def > 5: 
                obj.move_away(p=tg_obj.pos) # 躲避强敌
                print(info+'躲避强敌')
            else:
                # obj.wait() # 无所事事
                print(info+'无所事事')
            cnt+=1
            




screen_x = 1000
screen_y = 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption('Jungle')

w = World()
for _ in range(0,3):
    w.add_creature()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill('Honeydew')

    for obj in w.objs:
        pygame.draw.circle(screen, 'LawnGreen', (obj.pos.gx, obj.pos.gy), 10)
    
    w.run()


    pygame.display.flip()
    dt = clock.tick(60)