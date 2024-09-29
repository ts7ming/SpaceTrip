import pygame

class Cell:  
    def __init__(self, x, y, width, height, text, color=(255, 255, 255)):  
        self.rect = pygame.Rect(x, y, width, height)  
        self.color = color  
        self.text = text  
        self.font = pygame.font.Font(None, 16)  
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  
  
    def draw(self, screen):  
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


pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()


button_up = Cell(550,100,50,50,"Up","Wheat")
button_down = Cell(550,200,50,50,"Down","Wheat")
button_left = Cell(500,150,50,50,"Left","Wheat")
button_right = Cell(600,150,50,50,"Right","Wheat")

while True:
    go = False
    down_k = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]:
            down_k = 1
        elif pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2]:
            down_k = 2
        elif pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3]:
            pass


    screen.fill('Honeydew')
    button_up.draw(screen)
    button_down.draw(screen)
    button_left.draw(screen)
    button_right.draw(screen)

    # # 画格子
    
    g_size = 100
    g_margin = 10
    for i in range(1, N+1):
        line_width = 1
        pygame.draw.line(screen, 'black', (i * g_size - g_margin, g_size - g_margin), (i * g_size - g_margin, g_size * N - g_margin), line_width)
        pygame.draw.line(screen, 'black', (g_size - g_margin, i * g_size - g_margin), (g_size * N - g_margin, i * g_size - g_margin), line_width)


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
    button_right.dcolor = 'Wheat'