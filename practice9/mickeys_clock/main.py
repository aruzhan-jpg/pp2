import pygame
import os
import sys
import math
from datetime import datetime
from clock import get_time_angles

pygame.init()

WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, "images")


def load_and_scale(name, size=None):
    img = pygame.image.load(os.path.join(img_dir, name)).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


clock_bg = load_and_scale("mickey_clock.png", (420, 420))
mickey = load_and_scale("mickey.png", (150, 150))

# если обе руки одинаковые, можно использовать один и тот же файл
left_hand = load_and_scale("left_hand.png", (60, 150))
right_hand = load_and_scale("right_hand.png", (60, 150))

clock_bg_rect = clock_bg.get_rect(center=CENTER)
mickey_rect = mickey.get_rect(center=(CENTER[0], CENTER[1] + 5))

font = pygame.font.SysFont("Arial", 34, bold=True)


def blit_rotate_from_bottom_center(surf, image, center, angle):
    # ВАЖНО:
    # точка вращения — нижний центр картинки,
    # потому что у тебя палка идет вниз и должна начинаться из центра часов
    rotated_image = pygame.transform.rotate(image, angle)

    original_rect = image.get_rect()
    pivot = pygame.math.Vector2(0, original_rect.height // 2)

    rotated_offset = pivot.rotate(angle)

    rotated_rect = rotated_image.get_rect(center=(
        center[0] - rotated_offset.x,
        center[1] - rotated_offset.y
    ))

    surf.blit(rotated_image, rotated_rect)


def draw_second_hand(surf, center, angle):
    rad = math.radians(angle - 90)
    length = 100

    end_x = center[0] + math.cos(rad) * length
    end_y = center[1] + math.sin(rad) * length

    pygame.draw.line(surf, (255, 0, 0), center, (end_x, end_y), 2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    h_angle, m_angle, s_angle = get_time_angles()

    screen.fill((255, 255, 255))

    screen.blit(clock_bg, clock_bg_rect)
    screen.blit(mickey, mickey_rect)

    # правая рука = часовая
    blit_rotate_from_bottom_center(screen, right_hand, CENTER, h_angle)

    # левая рука = минутная
    blit_rotate_from_bottom_center(screen, left_hand, CENTER, m_angle)

    # секундная стрелка
    draw_second_hand(screen, CENTER, s_angle)

    pygame.draw.circle(screen, (0, 0, 0), CENTER, 5)

    current_time = datetime.now().strftime("%I:%M:%S")
    time_text = font.render(current_time, True, (0, 0, 0))
    text_rect = time_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(time_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()