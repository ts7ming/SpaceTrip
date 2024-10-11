import pygame
from random import choice, randint



class Pos:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else randint(0,World.map_size['x'])
        self.y = y if y is not None else randint(0,World.map_size['y'])
        self.gx = self.x
        self.gy = self.y

    def update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.gx = new_x
        self.gy = new_y



class Creature:
    def __init__(self):
        self.pos = Pos() # 位置
        self.search_distance = randint(100,500)  # 搜索距离
        self.attack_distance = randint(0,50) # 攻击距离
        self.Atk = randint(1,50) # 攻击力
        self.Def = randint(1,50) # 防御力
        self.Spd = randint(1,5) # 速度
        self.Hp = randint(50,80) # 生命

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
                obj.wait() # 无所事事
                print(info+'无所事事')
            elif obj.Atk - tg_obj.Def > 0:# and tg_obj.Atk - obj.Def<2:
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
                obj.wait() # 无所事事
                print(info+'无所事事')
            cnt+=1
            




screen_x = 1000
screen_y = 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption('Jungle')

w = World()
for _ in range(0,2):
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