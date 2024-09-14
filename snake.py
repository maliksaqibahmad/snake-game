import pygame
import random
import sys
import json
from enum import Enum, auto

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 60) // GRID_SIZE  # Reduce play area height to make room for info bar
DEFAULT_SPEED = 10
MIN_SPEED = 5
MAX_SPEED = 20
POWER_UP_DURATION = 300

# Colors
class Colors:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    YELLOW = (255, 255, 0)

# Directions
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Game States
class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SETTINGS = auto()
    GAME_OVER = auto()

class PowerUpType(Enum):
    SPEED = auto()
    INVINCIBILITY = auto()

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class PowerUp:
    def __init__(self, position, type):
        self.position = position
        self.type = type
        self.timer = 200  # Power-up disappears after 200 frames

    def draw(self, screen):
        color = Colors.BLUE if self.type == PowerUpType.SPEED else Colors.YELLOW
        pygame.draw.rect(screen, color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + 60, GRID_SIZE, GRID_SIZE))

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Xenzia")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.load_settings()
        self.game_state = GameState.MAIN_MENU
        self.create_menu_buttons()
        self.power_up = None
        self.power_up_effect = None
        self.power_up_timer = 0
        self.reset_game()

    def create_menu_buttons(self):
        self.start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 50, "Start Game", Colors.GREEN, Colors.WHITE)
        self.settings_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Settings", Colors.GRAY, Colors.WHITE)
        self.quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Quit", Colors.RED, Colors.WHITE)
        self.walls_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, f"Walls: {'On' if self.walls_on else 'Off'}", Colors.GREEN, Colors.WHITE)
        self.speed_up_button = Button(WIDTH // 2 + 50, HEIGHT // 2, 100, 50, "+", Colors.GREEN, Colors.WHITE)
        self.speed_down_button = Button(WIDTH // 2 - 150, HEIGHT // 2, 100, 50, "-", Colors.RED, Colors.WHITE)
        self.back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Back", Colors.GRAY, Colors.WHITE)
        self.restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Restart", Colors.GREEN, Colors.WHITE)
        self.menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Main Menu", Colors.BLUE, Colors.WHITE)

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.level = 1
        self.power_up = None
        self.power_up_effect = None
        self.power_up_timer = 0

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.walls_on = settings.get("walls_on", True)
                self.speed = settings.get("speed", DEFAULT_SPEED)
                self.high_score = settings.get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.walls_on = True
            self.speed = DEFAULT_SPEED
            self.high_score = 0

    def save_settings(self):
        settings = {
            "walls_on": self.walls_on,
            "speed": self.speed,
            "high_score": self.high_score
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake and (not self.power_up or food != self.power_up.position):
                return food

    def spawn_power_up(self):
        if random.random() < 0.1:  # 10% chance to spawn a power-up
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in self.snake and pos != self.food:
                    return PowerUp(pos, random.choice(list(PowerUpType)))
        return None

    def move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction.value[0], head[1] + self.direction.value[1])

        if self.walls_on and self.power_up_effect != PowerUpType.INVINCIBILITY:
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                return False  # Game over
        else:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in self.snake and self.power_up_effect != PowerUpType.INVINCIBILITY:
            return False  # Game over

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_settings()
            self.food = self.spawn_food()
            self.increase_difficulty()
            if not self.power_up:
                self.power_up = self.spawn_power_up()
        else:
            self.snake.pop()

        if self.power_up and new_head == self.power_up.position:
            self.activate_power_up()

        self.update_power_ups()

        return True

    def update_power_ups(self):
        if self.power_up:
            self.power_up.timer -= 1
            if self.power_up.timer <= 0:
                self.power_up = None

        if self.power_up_effect:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.deactivate_power_up()

    def activate_power_up(self):
        self.power_up_effect = self.power_up.type
        self.power_up_timer = POWER_UP_DURATION
        if self.power_up_effect == PowerUpType.SPEED:
            self.speed = min(self.speed + 2, MAX_SPEED)
        self.power_up = None

    def deactivate_power_up(self):
        if self.power_up_effect == PowerUpType.SPEED:
            self.speed = DEFAULT_SPEED
        self.power_up_effect = None

    def increase_difficulty(self):
        if self.score % 5 == 0:
            self.level += 1
            self.speed = min(self.speed + 1, MAX_SPEED)

    def draw_game(self):
        self.screen.fill(Colors.BLACK)

        # Draw info bar
        pygame.draw.rect(self.screen, Colors.GRAY, (0, 0, WIDTH, 60))
        self.draw_hud()

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = Colors.GREEN if self.power_up_effect != PowerUpType.INVINCIBILITY else (i * 10 % 256, i * 20 % 256, i * 30 % 256)
            pygame.draw.rect(self.screen, color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE + 60, GRID_SIZE, GRID_SIZE))

        # Draw food
        pygame.draw.rect(self.screen, Colors.RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE + 60, GRID_SIZE, GRID_SIZE))

        # Draw power-up
        if self.power_up:
            self.power_up.draw(self.screen)

        # Draw walls if enabled
        if self.walls_on:
            pygame.draw.rect(self.screen, Colors.WHITE, (0, 60, WIDTH, HEIGHT - 60), 2)

        pygame.display.flip()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, Colors.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, Colors.WHITE)
        speed_text = self.font.render(f"Speed: {self.speed}", True, Colors.WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 30))
        self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
        self.screen.blit(speed_text, (WIDTH - speed_text.get_width() - 10, 30))

    def handle_menu(self, pos):
        if self.game_state == GameState.MAIN_MENU:
            if self.start_button.is_clicked(pos):
                self.game_state = GameState.GAME
                self.reset_game()
            elif self.settings_button.is_clicked(pos):
                self.game_state = GameState.SETTINGS
            elif self.quit_button.is_clicked(pos):
                self.save_settings()
                pygame.quit()
                sys.exit()
        elif self.game_state == GameState.SETTINGS:
            if self.walls_button.is_clicked(pos):
                self.walls_on = not self.walls_on
                self.walls_button.text = f"Walls: {'On' if self.walls_on else 'Off'}"
            elif self.speed_up_button.is_clicked(pos):
                self.speed = min(self.speed + 1, MAX_SPEED)
            elif self.speed_down_button.is_clicked(pos):
                self.speed = max(self.speed - 1, MIN_SPEED)
            elif self.back_button.is_clicked(pos):
                self.game_state = GameState.MAIN_MENU
                self.save_settings()
        elif self.game_state == GameState.GAME_OVER:
            if self.restart_button.is_clicked(pos):
                self.game_state = GameState.GAME
                self.reset_game()
            elif self.menu_button.is_clicked(pos):
                self.game_state = GameState.MAIN_MENU

    def draw_menu(self):
        self.screen.fill(Colors.BLACK)

        if self.game_state == GameState.MAIN_MENU:
            self.start_button.draw(self.screen)
            self.settings_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        elif self.game_state == GameState.SETTINGS:
            self.walls_button.draw(self.screen)
            self.speed_up_button.draw(self.screen)
            self.speed_down_button.draw(self.screen)
            self.back_button.draw(self.screen)
            speed_text = self.font.render(f"Current Speed: {self.speed}", True, Colors.WHITE)
            self.screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 2 - 50))
        elif self.game_state == GameState.GAME_OVER:
            game_over_text = self.font.render("Game Over", True, Colors.RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, Colors.WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
            self.restart_button.draw(self.screen)
            self.menu_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_settings()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_menu(pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event)

            if self.game_state == GameState.GAME:
                if not self.move_snake():
                    self.game_state = GameState.GAME_OVER
                self.draw_game()
            else:
                self.draw_menu()

            self.clock.tick(self.speed)

    def handle_key_event(self, event):
        if self.game_state == GameState.GAME:
            if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
        elif event.key == pygame.K_ESCAPE:
            if self.game_state == GameState.GAME:
                self.game_state = GameState.MAIN_MENU
            elif self.game_state == GameState.SETTINGS:
                self.game_state = GameState.MAIN_MENU
                self.save_settings()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()