import pygame
import random
import sys
import os
import json

pygame.init()
pygame.mixer.init()

# -----------------------------
# WINDOW
# -----------------------------
WIDTH = 500
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
FPS = 120

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# -----------------------------
# ROAD / LANES
# -----------------------------
ROAD_LEFT = 120
ROAD_RIGHT = 380

lanes = [
    ROAD_LEFT + 40,
    (ROAD_LEFT + ROAD_RIGHT) // 2,
    ROAD_RIGHT - 40
]

# -----------------------------
# LEVELS
# -----------------------------
levels = {
    "easy": {
        "road_speed": 220,
        "player_speed": 340,
        "enemy_min": 250,
        "enemy_max": 350,
        "enemy_count": 3
    },
    "medium": {
        "road_speed": 300,
        "player_speed": 420,
        "enemy_min": 350,
        "enemy_max": 500,
        "enemy_count": 4
    },
    "hard": {
        "road_speed": 380,
        "player_speed": 500,
        "enemy_min": 500,
        "enemy_max": 700,
        "enemy_count": 5
    }
}

level_names = ["easy", "medium", "hard"]

# -----------------------------
# SAVE / LOAD JSON
# -----------------------------
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


default_settings = {
    "sound": True,
    "car_index": 0,
    "difficulty": "easy"
}

settings = load_json(SETTINGS_FILE, default_settings)

if "sound" not in settings:
    settings["sound"] = True
if "car_index" not in settings:
    settings["car_index"] = 0
if "difficulty" not in settings:
    settings["difficulty"] = "easy"

selected_level_index = level_names.index(settings["difficulty"])
current_level = settings["difficulty"]
garage_index = settings["car_index"]


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def save_leaderboard(data):
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_json(LEADERBOARD_FILE, data)


def add_score(username, score):
    leaderboard = load_leaderboard()
    leaderboard.append({
        "username": username,
        "score": score
    })
    save_leaderboard(leaderboard)


def get_best_score():
    leaderboard = load_leaderboard()
    if not leaderboard:
        return 0
    return max(item["score"] for item in leaderboard)


# -----------------------------
# SAFE LOAD HELPERS
# -----------------------------
def load_image(filename, size):
    path = os.path.join(IMAGES_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)


def safe_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None


# -----------------------------
# SOUNDS
# -----------------------------
menu_music_path = os.path.join(SOUNDS_DIR, "menu.mp3")
game_music_path = os.path.join(SOUNDS_DIR, "background.mp3")

crash_sound = safe_sound("crash.mp3")
coin_sound = safe_sound("coin.mp3")

if crash_sound:
    crash_sound.set_volume(0.7)
if coin_sound:
    coin_sound.set_volume(0.7)

pygame.mixer.music.set_volume(0.4)


def play_sound(sound):
    if settings["sound"] and sound:
        sound.play()


def play_music(path):
    if not settings["sound"]:
        pygame.mixer.music.stop()
        return

    if os.path.exists(path):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)


def play_menu_music():
    play_music(menu_music_path)


def play_game_music():
    play_music(game_music_path)


# -----------------------------
# LOAD IMAGES
# -----------------------------
road_img = pygame.image.load(os.path.join(IMAGES_DIR, "Road.jpg")).convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

player_skins = []
player_skin_files = [
    "main_car.jpg",
    "NPC1.jpg",
    "NPC2.jpg",
    "NPC3.jpg"
]

for skin_file in player_skin_files:
    player_skins.append(load_image(skin_file, (40, 70)))

npc_images = []
for i in range(1, 10):
    npc_images.append(load_image(f"NPC{i}.jpg", (40, 70)))

coin_images = {
    1: load_image("1coin.jpg", (25, 25)),
    3: load_image("3coin.jpg", (25, 25)),
    5: load_image("5coin.jpg", (25, 25)),
}

# Simple colored surfaces for obstacles and power-ups
def make_surface(size, color):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    return surf

obstacle_img = make_surface((45, 35), (120, 70, 30))
hazard_img = make_surface((50, 25), (200, 30, 30))

powerup_images = {
    "nitro": make_surface((28, 28), (0, 150, 255)),
    "shield": make_surface((28, 28), (80, 220, 120)),
    "repair": make_surface((28, 28), (255, 80, 80))
}

# -----------------------------
# FONTS
# -----------------------------
font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 40)
title_font = pygame.font.SysFont("Arial", 50)
menu_font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 22)

# -----------------------------
# GAME STATES
# -----------------------------
game_state = "username"
menu_options = ["PLAY", "LEADERBOARD", "SETTINGS", "EXIT"]
selected_menu_index = 0
settings_options = ["SOUND", "CAR COLOR", "DIFFICULTY", "BACK"]
selected_settings_index = 0
username = ""

# -----------------------------
# CREATE OBJECTS
# -----------------------------
def get_random_coin():
    roll = random.randint(1, 100)
    if roll <= 75:
        return 1
    elif roll <= 95:
        return 3
    return 5


def is_safe_position(x, y, objects, min_dist=120):
    for obj in objects:
        if abs(obj["y"] - y) < min_dist and abs(obj["x"] - x) < 35:
            return False
    return True


def create_enemy(level_name, bonus_speed=0):
    level = levels[level_name]
    return {
        "img": random.choice(npc_images),
        "x": random.choice(lanes) - 20,
        "y": random.randint(-900, -100),
        "target_lane": None,
        "current_speed": 0,
        "max_speed": random.uniform(level["enemy_min"], level["enemy_max"]) + bonus_speed,
        "acceleration": random.uniform(1.5, 2.5)
    }


def create_obstacle():
    kind = random.choice(["barrier", "hazard"])
    return {
        "type": kind,
        "x": random.choice(lanes) - 22,
        "y": random.randint(-1000, -250),
        "speed": random.uniform(260, 420)
    }


def create_powerup():
    return {
        "type": random.choice(["nitro", "shield", "repair"]),
        "x": random.choice(lanes) - 14,
        "y": random.randint(-1400, -500),
        "speed": random.uniform(230, 350)
    }


def respawn_coin(state):
    while True:
        new_x = random.choice(lanes) - 12
        new_y = random.randint(-350, -100)
        objects = state["enemies"] + state["obstacles"]

        if is_safe_position(new_x, new_y, objects, 90):
            state["coin_x"] = new_x
            state["coin_y"] = new_y
            state["coin_value"] = get_random_coin()
            break


def reset_game(level_name):
    enemies = []

    for _ in range(levels[level_name]["enemy_count"]):
        while True:
            e = create_enemy(level_name)
            if is_safe_position(e["x"], e["y"], enemies):
                enemies.append(e)
                break

    return {
        "player_x": lanes[1] - 20,
        "player_y": HEIGHT - 100,

        "enemies": enemies,
        "obstacles": [create_obstacle(), create_obstacle()],
        "powerups": [create_powerup()],

        "coin_value": get_random_coin(),
        "coin_x": random.choice(lanes) - 12,
        "coin_y": -200,
        "coin_speed": 5,

        "road_y1": 0.0,
        "road_y2": -HEIGHT,

        "coins": 0,
        "score": 0,
        "health": 3,
        "shield": False,
        "nitro_timer": 0,
        "game_over": False,
        "saved_to_leaderboard": False,
        "level": level_name,
        "skin_index": garage_index,
        "speed": 0,
        "distance": 0
    }


state = None


def finish_game():
    global state

    if state and not state["game_over"]:
        state["game_over"] = True
        pygame.mixer.music.stop()
        play_sound(crash_sound)

    if state and not state["saved_to_leaderboard"]:
        add_score(username if username else "Player", state["score"])
        state["saved_to_leaderboard"] = True


def damage_player():
    if state["shield"]:
        state["shield"] = False
        return

    state["health"] -= 1
    play_sound(crash_sound)

    if state["health"] <= 0:
        finish_game()


def save_current_settings():
    settings["sound"] = bool(settings["sound"])
    settings["car_index"] = garage_index
    settings["difficulty"] = current_level
    save_json(SETTINGS_FILE, settings)


# -----------------------------
# START MUSIC
# -----------------------------
play_menu_music()
running = True

# =====================================
# LOOP
# =====================================
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_current_settings()
            running = False

        if event.type == pygame.KEYDOWN:

            # USERNAME SCREEN
            if game_state == "username":
                if event.key == pygame.K_RETURN and username.strip():
                    game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 12 and event.unicode.isprintable():
                    username += event.unicode

            # MAIN MENU
            elif game_state == "menu":
                if event.key == pygame.K_UP:
                    selected_menu_index = (selected_menu_index - 1) % len(menu_options)

                elif event.key == pygame.K_DOWN:
                    selected_menu_index = (selected_menu_index + 1) % len(menu_options)

                elif event.key == pygame.K_RETURN:
                    selected_option = menu_options[selected_menu_index]

                    if selected_option == "PLAY":
                        state = reset_game(current_level)
                        game_state = "playing"
                        play_game_music()

                    elif selected_option == "LEADERBOARD":
                        game_state = "leaderboard"

                    elif selected_option == "SETTINGS":
                        game_state = "settings"

                    elif selected_option == "EXIT":
                        save_current_settings()
                        running = False

            # SETTINGS
            elif game_state == "settings":
                if event.key == pygame.K_UP:
                    selected_settings_index = (selected_settings_index - 1) % len(settings_options)

                elif event.key == pygame.K_DOWN:
                    selected_settings_index = (selected_settings_index + 1) % len(settings_options)

                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN]:
                    option = settings_options[selected_settings_index]

                    if option == "SOUND":
                        settings["sound"] = not settings["sound"]
                        if settings["sound"]:
                            play_menu_music()
                        else:
                            pygame.mixer.music.stop()

                    elif option == "CAR COLOR":
                        garage_index = (garage_index + 1) % len(player_skins)

                    elif option == "DIFFICULTY":
                        selected_level_index = level_names.index(current_level)
                        if event.key == pygame.K_LEFT:
                            selected_level_index = (selected_level_index - 1) % len(level_names)
                        else:
                            selected_level_index = (selected_level_index + 1) % len(level_names)
                        current_level = level_names[selected_level_index]

                    elif option == "BACK":
                        save_current_settings()
                        game_state = "menu"

                elif event.key == pygame.K_ESCAPE:
                    save_current_settings()
                    game_state = "menu"

            # LEADERBOARD
            elif game_state == "leaderboard":
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    game_state = "menu"

            # PLAYING
            elif game_state == "playing":
                if state["game_over"] and event.key == pygame.K_r:
                    state = reset_game(state["level"])
                    play_game_music()

                elif state["game_over"] and event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    state = None
                    play_menu_music()

    keys = pygame.key.get_pressed()

    # -----------------------------
    # UPDATE GAME
    # -----------------------------
    if game_state == "playing" and not state["game_over"]:

        base_level = levels[state["level"]]

        # Dynamic difficulty scaling
        difficulty_bonus = state["score"] * 8 + state["distance"] * 0.01

        player_speed = base_level["player_speed"]
        road_base_speed = base_level["road_speed"] + difficulty_bonus

        # GAS / BRAKE
        speed_multiplier = 1.0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            speed_multiplier = 1.45

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            speed_multiplier = 0.55

        if state["nitro_timer"] > 0:
            speed_multiplier *= 1.6
            state["nitro_timer"] -= dt

        road_base_speed *= speed_multiplier
        player_speed *= speed_multiplier
        state["speed"] = int(road_base_speed)
        state["distance"] += road_base_speed * dt

        # PLAYER MOVE
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            state["player_x"] -= player_speed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            state["player_x"] += player_speed * dt

        # ROAD LIMIT = lane hazard
        if state["player_x"] < ROAD_LEFT or state["player_x"] > ROAD_RIGHT - 40:
            damage_player()
            state["player_x"] = max(ROAD_LEFT, min(state["player_x"], ROAD_RIGHT - 40))

        # ROAD SCROLL
        road_speed = road_base_speed * dt
        state["road_y1"] += road_speed
        state["road_y2"] += road_speed

        if state["road_y1"] >= HEIGHT:
            state["road_y1"] = -HEIGHT
        if state["road_y2"] >= HEIGHT:
            state["road_y2"] = -HEIGHT

        # ENEMIES
        for enemy in state["enemies"]:
            target_speed = (enemy["max_speed"] + difficulty_bonus) * speed_multiplier

            for other in state["enemies"]:
                if other == enemy:
                    continue

                same_lane = abs(enemy["x"] - other["x"]) < 5
                in_front = other["y"] > enemy["y"]
                close = other["y"] - enemy["y"] < 120

                if same_lane and in_front and close:
                    target_speed = other["current_speed"] * 0.8

                    if enemy["target_lane"] is None:
                        possible = [l for l in lanes if abs((l - 20) - enemy["x"]) > 5]

                        for lane in possible:
                            lane_x = lane - 20
                            free = True
                            for e in state["enemies"]:
                                if abs(e["x"] - lane_x) < 5 and abs(e["y"] - enemy["y"]) < 120:
                                    free = False
                                    break
                            if free:
                                enemy["target_lane"] = lane_x
                                break
                    break

            enemy["current_speed"] += (target_speed - enemy["current_speed"]) * enemy["acceleration"] * dt
            enemy["y"] += enemy["current_speed"] * dt

            if enemy["target_lane"] is not None:
                enemy["x"] += (enemy["target_lane"] - enemy["x"]) * 4 * dt
                if abs(enemy["target_lane"] - enemy["x"]) < 2:
                    enemy["target_lane"] = None

            if enemy["y"] > HEIGHT:
                while True:
                    new_enemy = create_enemy(state["level"], difficulty_bonus)
                    if is_safe_position(new_enemy["x"], new_enemy["y"], state["enemies"]):
                        enemy.update(new_enemy)
                        state["score"] += 1
                        break

        # COIN
        state["coin_y"] += state["coin_speed"] * 60 * dt * speed_multiplier

        if state["coin_y"] > HEIGHT:
            respawn_coin(state)

        # OBSTACLES / HAZARDS
        for obstacle in state["obstacles"]:
            obstacle["y"] += (obstacle["speed"] + difficulty_bonus) * dt * speed_multiplier

            if obstacle["y"] > HEIGHT:
                obstacle.update(create_obstacle())

        # POWERUPS
        for powerup in state["powerups"]:
            powerup["y"] += powerup["speed"] * dt * speed_multiplier

            if powerup["y"] > HEIGHT:
                powerup.update(create_powerup())

        # COLLISIONS
        player_rect = pygame.Rect(state["player_x"], state["player_y"], 40, 70)

        for enemy in state["enemies"]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 40, 70)
            if player_rect.colliderect(enemy_rect):
                damage_player()
                enemy.update(create_enemy(state["level"], difficulty_bonus))

        for obstacle in state["obstacles"]:
            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], 45, 35)
            if player_rect.colliderect(obstacle_rect):
                damage_player()
                obstacle.update(create_obstacle())

        coin_rect = pygame.Rect(state["coin_x"], state["coin_y"], 25, 25)
        if player_rect.colliderect(coin_rect):
            play_sound(coin_sound)
            state["coins"] += state["coin_value"]
            state["score"] += state["coin_value"]
            respawn_coin(state)

        for powerup in state["powerups"]:
            powerup_rect = pygame.Rect(powerup["x"], powerup["y"], 28, 28)

            if player_rect.colliderect(powerup_rect):
                if powerup["type"] == "nitro":
                    state["nitro_timer"] = 4

                elif powerup["type"] == "shield":
                    state["shield"] = True

                elif powerup["type"] == "repair":
                    state["health"] = min(3, state["health"] + 1)

                powerup.update(create_powerup())

    # -----------------------------
    # DRAW
    # -----------------------------
    screen.fill((20, 20, 20))

    # USERNAME SCREEN
    if game_state == "username":
        title_text = title_font.render("RACER", True, (255, 255, 255))
        ask_text = small_font.render("Enter username and press ENTER", True, (200, 200, 200))
        username_text = menu_font.render(username + "|", True, (255, 255, 0))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 180))
        screen.blit(ask_text, (WIDTH // 2 - ask_text.get_width() // 2, 300))
        screen.blit(username_text, (WIDTH // 2 - username_text.get_width() // 2, 360))

    # MAIN MENU
    elif game_state == "menu":
        title_text = title_font.render("RACER", True, (255, 255, 255))
        info_text = small_font.render("UP/DOWN - menu   ENTER - choose", True, (180, 180, 180))
        user_text = small_font.render(f"Player: {username}", True, (220, 220, 220))
        best_menu_text = small_font.render(f"Best score: {get_best_score()}", True, (220, 220, 220))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 110))
        screen.blit(user_text, (WIDTH // 2 - user_text.get_width() // 2, 180))

        for i, option in enumerate(menu_options):
            color = (255, 255, 0) if i == selected_menu_index else (255, 255, 255)
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 270 + i * 65))

        screen.blit(best_menu_text, (WIDTH // 2 - best_menu_text.get_width() // 2, 570))
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 620))

    # SETTINGS SCREEN
    elif game_state == "settings":
        title_text = title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        values = {
            "SOUND": "ON" if settings["sound"] else "OFF",
            "CAR COLOR": f"CAR {garage_index + 1}",
            "DIFFICULTY": current_level.upper(),
            "BACK": ""
        }

        for i, option in enumerate(settings_options):
            color = (255, 255, 0) if i == selected_settings_index else (255, 255, 255)
            text = f"{option}: {values[option]}" if values[option] else option
            option_text = menu_font.render(text, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 240 + i * 70))

        screen.blit(player_skins[garage_index], (WIDTH // 2 - 20, 560))

    # LEADERBOARD SCREEN
    elif game_state == "leaderboard":
        title_text = title_font.render("TOP 10", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))

        leaderboard = load_leaderboard()

        if not leaderboard:
            empty_text = small_font.render("No scores yet", True, (220, 220, 220))
            screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, 220))
        else:
            for i, item in enumerate(leaderboard[:10]):
                row = small_font.render(
                    f"{i + 1}. {item['username']} — {item['score']}",
                    True,
                    (255, 255, 255)
                )
                screen.blit(row, (110, 170 + i * 42))

        back_text = small_font.render("ESC / ENTER - back", True, (180, 180, 180))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 700))

    # PLAYING SCREEN
    elif game_state == "playing":
        screen.blit(road_img, (0, int(state["road_y1"])))
        screen.blit(road_img, (0, int(state["road_y2"])))

        # obstacles
        for obstacle in state["obstacles"]:
            img = hazard_img if obstacle["type"] == "hazard" else obstacle_img
            screen.blit(img, (obstacle["x"], obstacle["y"]))

        # coins
        coin_img = coin_images[state["coin_value"]]
        screen.blit(coin_img, (state["coin_x"], state["coin_y"]))

        # powerups
        for powerup in state["powerups"]:
            screen.blit(powerup_images[powerup["type"]], (powerup["x"], powerup["y"]))

            label = small_font.render(powerup["type"][0].upper(), True, (255, 255, 255))
            screen.blit(label, (powerup["x"] + 7, powerup["y"] + 2))

        # player
        screen.blit(player_skins[state["skin_index"]], (state["player_x"], state["player_y"]))

        # shield outline
        if state["shield"]:
            pygame.draw.circle(
                screen,
                (80, 220, 120),
                (int(state["player_x"] + 20), int(state["player_y"] + 35)),
                45,
                3
            )

        # enemies
        for enemy in state["enemies"]:
            screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

        # UI
        score_text = font.render(f"Score: {state['score']}", True, (255, 255, 255))
        coins_text = font.render(f"Coins: {state['coins']}", True, (255, 255, 255))
        level_text = font.render(f"Level: {state['level'].upper()}", True, (255, 255, 255))
        speed_text = font.render(f"Speed: {state['speed']}", True, (255, 255, 255))
        health_text = font.render(f"HP: {state['health']}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (WIDTH - coins_text.get_width() - 10, 10))
        screen.blit(level_text, (10, 45))
        screen.blit(speed_text, (10, 80))
        screen.blit(health_text, (WIDTH - health_text.get_width() - 10, 45))

        if state["nitro_timer"] > 0:
            nitro_text = small_font.render("NITRO ACTIVE", True, (255, 255, 0))
            screen.blit(nitro_text, (WIDTH // 2 - nitro_text.get_width() // 2, 20))

        if state["game_over"]:
            text1 = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text2 = small_font.render("Press R to restart", True, (255, 255, 255))
            text3 = small_font.render("Press ESC for menu", True, (255, 255, 255))
            text4 = small_font.render("Score saved to leaderboard.json", True, (255, 255, 0))

            screen.blit(text1, (
                WIDTH // 2 - text1.get_width() // 2,
                HEIGHT // 2 - 80
            ))
            screen.blit(text4, (
                WIDTH // 2 - text4.get_width() // 2,
                HEIGHT // 2 - 25
            ))
            screen.blit(text2, (
                WIDTH // 2 - text2.get_width() // 2,
                HEIGHT // 2 + 15
            ))
            screen.blit(text3, (
                WIDTH // 2 - text3.get_width() // 2,
                HEIGHT // 2 + 50
            ))

    pygame.display.update()

save_current_settings()
pygame.quit()
sys.exit()
