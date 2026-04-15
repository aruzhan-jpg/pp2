import pygame
from ball import BallGame


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Moving Ball")

    clock = pygame.time.Clock()
    game = BallGame(screen)

    running = True
    while running:
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_up()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                elif event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()