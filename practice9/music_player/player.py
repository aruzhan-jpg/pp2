import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.playlist = [
            os.path.join("music", "sample_tracks", "track1.wav"),
            os.path.join("music", "sample_tracks", "track2.wav"),
        ]

        self.current_track_index = 0
        self.is_playing = False

        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.main_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

    def load_track(self):
        pygame.mixer.music.load(self.playlist[self.current_track_index])

    def play_music(self):
        self.load_track()
        pygame.mixer.music.play()
        self.is_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_music()

    def previous_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_music()

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_track_index])

    def get_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms / 1000

    def get_track_length(self):
        track_path = self.playlist[self.current_track_index]
        sound = pygame.mixer.Sound(track_path)
        return sound.get_length()

    def draw_progress_bar(self, screen, x, y, width, height):
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=8)

        current_pos = self.get_position_seconds()
        total_length = self.get_track_length()

        if total_length > 0:
            progress_ratio = min(current_pos / total_length, 1)
        else:
            progress_ratio = 0

        progress_width = int(width * progress_ratio)

        pygame.draw.rect(
            screen,
            (70, 130, 180),
            (x, y, progress_width, height),
            border_radius=8
        )

    def draw_button_box(self, screen, x, y, w, h, text):
        pygame.draw.rect(screen, (245, 245, 245), (x, y, w, h), border_radius=12)
        pygame.draw.rect(screen, (180, 180, 180), (x, y, w, h), 2, border_radius=12)

        text_surface = self.small_font.render(text, True, (30, 30, 30))
        text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(text_surface, text_rect)

    def draw_ui(self, screen):
        screen.fill((235, 240, 245))

        pygame.draw.rect(screen, (255, 255, 255), (90, 70, 620, 460), border_radius=25)
        pygame.draw.rect(screen, (210, 210, 210), (90, 70, 620, 460), 2, border_radius=25)

        title = self.title_font.render("Music Player", True, (35, 35, 35))
        screen.blit(title, (280, 95))

        pygame.draw.rect(screen, (225, 232, 240), (140, 170, 520, 80), border_radius=18)

        track_title = self.main_font.render("Now Playing:", True, (80, 80, 80))
        track_name = self.main_font.render(self.get_current_track_name(), True, (20, 60, 140))
        screen.blit(track_title, (165, 185))
        screen.blit(track_name, (165, 215))

        status_text = "Playing" if self.is_playing else "Stopped"
        status_color = (0, 140, 70) if self.is_playing else (180, 50, 50)
        status_surface = self.main_font.render(f"Status: {status_text}", True, status_color)
        screen.blit(status_surface, (165, 280))

        current_pos = int(self.get_position_seconds())
        total_length = int(self.get_track_length())

        position_surface = self.main_font.render(
            f"Position: {current_pos} / {total_length} sec",
            True,
            (60, 60, 60)
        )
        screen.blit(position_surface, (165, 325))

        self.draw_progress_bar(screen, 165, 375, 390, 18)

        controls_title = self.main_font.render("Controls", True, (40, 40, 40))
        screen.blit(controls_title, (165, 425))

        self.draw_button_box(screen, 165, 465, 90, 42, "P - Play")
        self.draw_button_box(screen, 270, 465, 90, 42, "S - Stop")
        self.draw_button_box(screen, 375, 465, 90, 42, "N - Next")
        self.draw_button_box(screen, 480, 465, 115, 42, "B - Previous")
        self.draw_button_box(screen, 610, 465, 70, 42, "Q - Quit")

        pygame.display.flip()