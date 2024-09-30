import pygame
from random import choice, randint

class Cell:  
    def __init__(self, x, y, width, height, text, color=(255, 255, 255)):  
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.value = int(text)

        self.map = {
            -4:'Left',
            -6:'Right',
            -2:'Down',
            -8:'Up',
            0:''
        }
        if text in self.map:
            self.text = self.map[text]
        else:
            self.text = str(text)


    def set_v(self, v):
        self.value = v
        if v in self.map:
            self.text = self.map[v]
        else:
            self.text = str(v)
    
    def get_v(self):
        return self.value
  
    def draw(self, screen):
        if self.value>0:
            self.font = pygame.font.Font(None, self.value+20)
        else:
            self.font = pygame.font.Font(None, 16)
        self.text_surface = self.font.render(self.text, True, (160,82,45))  
        pygame.draw.rect(screen, self.color, self.rect)  
        screen.blit(self.text_surface, (self.rect.left + (self.rect.width - self.text_surface.get_width()) // 2,  
                                        self.rect.top + (self.rect.height - self.text_surface.get_height()) // 2))  
  
    def is_clicked(self, event):  
        if event.type == pygame.MOUSEBUTTONDOWN:  
            mouse_pos = event.pos  
            if self.rect.collidepoint(mouse_pos):  
                return True  
        return False
    
    def move(self):
        pass


screen_x = 1200
screen_y = 800

N = 5

g_size = 100
g_margin = 50

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

vl = N*g_size
button_up = Cell(vl+50,100,50,50,-8,"Wheat")
button_down = Cell(vl+50,200,50,50,-2,"Wheat")
button_left = Cell(vl,150,50,50,-4,"Wheat")
button_right = Cell(vl+100,150,50,50,-6,"Wheat")

board = {}
for i in range(1,N):
    for j in range(1,N):
        board[str(i)+str(j)] = Cell(j*g_size-g_margin+5,i*g_size-g_margin+5,90,90,0,(222,184,135))

def update_board():
    # 随机值
    empty_num = 1
    empty_cell = []
    max_cell = 1
    for idx, bd in board.items():
        if bd.value == 0:
            empty_num+=1
            empty_cell.append(idx)
        else:
            if bd.value > max_cell:
                max_cell = bd.value
    max_cell = max(3,max_cell)/2
    t_idx = choice(empty_cell)
    # board[t_idx].set_v(choice([x for x in [1,2,4,8,16,32,64,128,256] if x<=max_cell]))
    board[t_idx].set_v(1)


def move_board(d):
    stp = 0
    if d == 'left':
        do = True
        while do:
            cnt = 0
            for ii in range(1, N):
                for jj in range(2, N):
                    if board[str(ii)+str(jj)].value == 0:
                        continue
                    elif board[str(ii)+str(jj-1)].value == 0:
                        board[str(ii)+str(jj-1)].set_v(board[str(ii)+str(jj)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    elif board[str(ii)+str(jj)].value == board[str(ii)+str(jj-1)].value:
                        board[str(ii)+str(jj-1)].set_v(board[str(ii)+str(jj)].value + board[str(ii)+str(jj-1)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    else:
                        continue
            if cnt==0:
                do = False
    elif d == 'right':
        do = True
        while do:
            cnt = 0
            for ii in range(1, N):
                for jj in sorted(range(1, N-1),reverse=True):
                    if board[str(ii)+str(jj)].value == 0:
                        continue
                    elif board[str(ii)+str(jj+1)].value == 0:
                        board[str(ii)+str(jj+1)].value = board[str(ii)+str(jj)].value
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    elif board[str(ii)+str(jj)].value == board[str(ii)+str(jj+1)].value:
                        board[str(ii)+str(jj+1)].set_v(board[str(ii)+str(jj)].value + board[str(ii)+str(jj+1)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    else:
                        continue
            if cnt==0:
                do = False
    elif d == 'up':
        do = True
        while do:
            cnt = 0
            for ii in range(2, N):
                for jj in range(1, N):
                    if board[str(ii)+str(jj)].value == 0:
                        continue
                    elif board[str(ii-1)+str(jj)].value == 0:
                        board[str(ii-1)+str(jj)].value = board[str(ii)+str(jj)].value
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    elif board[str(ii)+str(jj)].value == board[str(ii-1)+str(jj)].value:
                        board[str(ii-1)+str(jj)].set_v(board[str(ii)+str(jj)].value + board[str(ii-1)+str(jj)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    else:
                        continue
            if cnt==0:
                do = False
    elif d == 'down':
        do = True
        while do:
            cnt = 0
            for ii in sorted(range(1, N-1),reverse=True):
                for jj in range(1, N):
                    if board[str(ii)+str(jj)].value == 0:
                        continue
                    elif board[str(ii+1)+str(jj)].value == 0:
                        board[str(ii+1)+str(jj)].set_v(board[str(ii)+str(jj)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    elif board[str(ii)+str(jj)].value == board[str(ii+1)+str(jj)].value:
                        board[str(ii+1)+str(jj)].set_v(board[str(ii)+str(jj)].value + board[str(ii+1)+str(jj)].value)
                        board[str(ii)+str(jj)].set_v(0)
                        cnt+=1
                        stp+=0
                    else:
                        continue
            if cnt==0:
                do = False
    else:
        pass
    if stp>0:
        return True
    else:
        return False

update_board()

# board['24'].set_v(2)
# board['23'].set_v(2)
# board['14'].set_v(2)

while True:
    go = False
    down_k = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif button_up.is_clicked(event):
            if move_board(d='up'):
                update_board()
        elif button_down.is_clicked(event):
            if move_board(d='down'):
                update_board()
        elif button_left.is_clicked(event):
            if move_board(d='left'):
                update_board()
        elif button_right.is_clicked(event):
            if move_board(d='right'):
                update_board()




    screen.fill('Honeydew')
    button_up.draw(screen)
    button_down.draw(screen)
    button_left.draw(screen)
    button_right.draw(screen)

    for i in range(1, N+1):
        line_width = 1
        pygame.draw.line(screen, 'black', (i * g_size - g_margin, g_size - g_margin), (i * g_size - g_margin, g_size * N - g_margin), line_width)
        pygame.draw.line(screen, 'black', (g_size - g_margin, i * g_size - g_margin), (g_size * N - g_margin, i * g_size - g_margin), line_width)



    for idx, bd in board.items():
        bd.draw(screen)

    # # 概况信息
    # info_list = ['step:  ' + str(count), ''] + msg_display
    # pi = pos['msg'][1]
    # for info in info_list:
    #     font = pygame.font.SysFont("Arial", size['cell_radius_draft'])
    #     txt = font.render(info, True, color['msg'])
    #     screen.blit(txt, (pos['msg'][0], pi))
    #     pi += 15
    pygame.display.flip()
    dt = clock.tick(30)

    button_up.color = 'Wheat'
    button_down.color = 'Wheat'
    button_left.color = 'Wheat'
    button_right.color = 'Wheat'