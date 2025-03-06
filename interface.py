# manage graphic interface and user events
import pygame

class Interface:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Graphic Comp.")
        self.running = True
        self.pixels = []  # stores drawn objects

        # button config
        self.button_color = (0, 0, 0)
        self.button_rect = pygame.Rect(10, 10, 100, 40)  # (x, y, width, height)
        self.clear_text = pygame.font.Font(None, 30).render("Clear", True, (255, 255, 255))

    def draw_pixel(self, x, y, color=(255, 255, 255)):
        # add pixel to array if it's inside the canvas
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels.append((x, y, color))

    def handle_events(self):
        # handles user interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # click
                x, y = event.pos

                if self.button_rect.collidepoint(x, y):
                    #print("Clear button clicked!")
                    self.pixels.clear()  # clear all drawn pixels
                else:
                    #print(f"Mouse clicked at ({x}, {y})")
                    self.draw_pixel(x, y, (255, 0, 0)) # draw red pixel

    def update(self):
        # update screen
        self.screen.fill((255, 255, 255)) # white bg
        self.clear_button()

        # change cursor to hand when hovering over the button
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # change cursor to hand
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # default cursor

        for x, y, color in self.pixels:  # draw all stored pixels
            self.screen.set_at((x, y), color)
        pygame.display.flip()

    def clear_button(self):
        # set clear button
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        self.screen.blit(self.clear_text, (self.button_rect.x + 20, self.button_rect.y + 10))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()

        pygame.quit()
