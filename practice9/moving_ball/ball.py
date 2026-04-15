import pygame


class BallGame:
    def __init__(self, screen):
        self.screen = screen
        self.width = 800
        self.height = 600

        self.background_color = (255, 255, 255)
        self.ball_color = (255, 0, 0)

        self.radius = 25
        self.step = 20

        self.x = self.width // 2
        self.y = self.height // 2

    def move_up(self):
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step

    def move_down(self):
        if self.y + self.step + self.radius <= self.height:
            self.y += self.step

    def move_left(self):
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step

    def move_right(self):
        if self.x + self.step + self.radius <= self.width:
            self.x += self.step

    def draw(self):
        self.screen.fill(self.background_color)
        pygame.draw.circle(self.screen, self.ball_color, (self.x, self.y), self.radius)
        pygame.display.flip()