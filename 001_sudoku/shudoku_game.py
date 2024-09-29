import pygame
import sudokum


class Button:
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


class Sudoku:
    def __init__(self):
        self.board = None
    
    def new_game(self, mask_rate=0.5):
        self.board = sudokum.generate(mask_rate=mask_rate)
