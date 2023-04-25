import pygame
from Board import Board


class SudokuGame:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku")
        self.reset_button = pygame.Rect(20, 480, 100, 30)
        self.restart_button = pygame.Rect(170, 480, 100, 30)
        self.exit_button = pygame.Rect(320, 480, 100, 30)
        self.board = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.buttons_shown = False
        self.background_image = pygame.image.load("background_image/image.png").convert()

    def run(self):
        self.welcome_screen()
        self.difficulty = 30  # set a default value for self.difficulty
        self.board = Board(self.width, self.height, self.screen, self.difficulty)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        self.move_selection(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_selection(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.move_selection(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_selection(1, 0)
                    elif event.key == pygame.K_0:
                        self.board.place_number(0)
                    elif event.key == pygame.K_1:
                        self.board.place_number(1)
                    elif event.key == pygame.K_2:
                        self.board.place_number(2)
                    elif event.key == pygame.K_3:
                        self.board.place_number(3)
                    elif event.key == pygame.K_4:
                        self.board.place_number(4)
                    elif event.key == pygame.K_5:
                        self.board.place_number(5)
                    elif event.key == pygame.K_6:
                        self.board.place_number(6)
                    elif event.key == pygame.K_7:
                        self.board.place_number(7)
                    elif event.key == pygame.K_8:
                        self.board.place_number(8)
                    elif event.key == pygame.K_9:
                        self.board.place_number(9)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.board.clear()
                    elif event.key == pygame.K_RETURN:
                        if self.board.selected_cell:
                            self.board.sketch(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        cell = self.board.click(*pos)
                        if cell:
                            self.board.select_cell(*cell)

                        if self.reset_button.collidepoint(pos):
                            self.board = Board(self.width, self.height, self.screen, self.difficulty)
                        if self.restart_button.collidepoint(pos):
                            self.welcome_screen()
                            self.board = Board(self.width, self.height, self.screen, self.difficulty)
                        if self.exit_button.collidepoint(pos):
                            self.running = False

                if self.board.is_full() and self.board.check_board():
                    self.display_result(1)
                    self.running = False
                elif self.board.is_full() and not self.board.check_board():
                    self.display_result(0)
                    self.running = False

            self.screen.fill((173, 216, 230))
            self.board.draw()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_buttons(self):
        self.draw_custom_button("Reset", 20, 480, 100, 30, (50, 70, 255), (0, 0, 0))

        # Restart button
        self.draw_custom_button("Restart", 170, 480, 100, 30, (0, 255, 0), (0, 0, 0))

        # Exit button
        self.draw_custom_button("Exit", 320, 480, 100, 30, (255, 0, 0), (0, 0, 0))

    def move_selection(self, dx, dy):
        if self.board.selected_cell:
            row, col = self.board.selected_cell
            new_row = (row + dy) % 9
            new_col = (col + dx) % 9
            self.board.select_cell(new_row, new_col)

    def welcome_screen(self):

        font = pygame.font.Font(None, 36)
        title_text = font.render("Welcome to Sudoku Game", True, (0, 0, 0))
        title_text2 = font.render("Select Game mode", True, (0, 0, 0))
        easy_text = font.render("Easy", True, (0, 0, 0))
        medium_text = font.render("Medium", True, (0, 0, 0))
        hard_text = font.render("Hard", True, (0, 0, 0))

        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))
        title2_rect = title_text2.get_rect(center=(self.width // 2, self.height // 4 + 80))
        easy_rect = easy_text.get_rect(center=(self.width // 5, self.height // 2))
        medium_rect = medium_text.get_rect(center=(self.width // 2, self.height // 2 ))
        hard_rect = hard_text.get_rect(center=(self.width // 1.5 + 69, self.height // 2))

        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(title_text2, title2_rect)
            self.screen.blit(easy_text, easy_rect)
            self.screen.blit(medium_text, medium_rect)
            self.screen.blit(hard_text, hard_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos):
                        self.difficulty = 30
                        return
                    elif medium_rect.collidepoint(event.pos):
                        self.difficulty = 40
                        return
                    elif hard_rect.collidepoint(event.pos):
                        self.difficulty = 50
                        return

    def draw_custom_button(self, text, x, y, width, height, color, outline_color=None, font_size=20):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect)

        if outline_color is not None:
            outline_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
            pygame.draw.rect(self.screen, outline_color, outline_rect, 2)

        button_text = pygame.font.SysFont("Arial", font_size).render(text, True, (0, 0, 0))
        text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(button_text, text_rect)

    def display_result(self, result):
        font = pygame.font.Font(None, 36)
        if result == 1:
            text = font.render("Congratulations! You won!", True, (0, 0, 0))
        else:
            text = font.render("Sorry, you lost. Please try again!", True, (0, 0, 0))

        rect = text.get_rect(center=(self.width // 2, self.height // 8))

        if result == 1:
            button_text = "Exit"
        else:
            button_text = "Restart"

        button_font = pygame.font.SysFont("Arial", 20)
        button_text_render = button_font.render(button_text, True, (0, 0, 0))

        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(text, rect)

            self.draw_custom_button("Restart", self.width // 2 - 120, self.height // 2, 100, 30, (0, 255, 0), (0, 0, 0))
            self.draw_custom_button("Exit", self.width // 2 + 20, self.height // 2, 100, 30, (255, 0, 0), (0, 0, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    restart_button = pygame.Rect(self.width // 2 - 120, self.height // 2, 100, 30)
                    exit_button = pygame.Rect(self.width // 2 + 20, self.height // 2, 100, 30)

                    if restart_button.collidepoint(event.pos):
                        self.running = False
                        main()
                        self.board = Board(self.width, self.height, self.screen, self.difficulty)
                        return
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()


def main():
    pygame.init()
    game = SudokuGame(453.56, 560)
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
