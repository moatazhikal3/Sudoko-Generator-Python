import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.width = 50
        self.height = 50
        self.selected = False
        self.readonly = value != 0

    def set_cell_value(self, value):
        self.value = value
        self.readonly = value != 0

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        font_size = 25
        font = pygame.font.SysFont('Arial', font_size)

        x = self.col * self.width
        y = self.row * self.height

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.width / 2, y + self.height / 2))
            self.screen.blit(text, text_rect)

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x, y, self.width, self.height), 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x, y, self.width, self.height), 1)
