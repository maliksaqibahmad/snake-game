"""
Snake Xenzia Game

This script implements an enhanced version of the classic Snake game using Pygame.
Features include adjustable speed, difficulty levels, power-ups, and more.

Requirements:
- Python 3.x
- Pygame library

To run the game, execute this script and use the menu to start the game.
Use arrow keys to control the snake during gameplay.

Author: Claude
Date: September 13, 2024
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
DEFAULT_SPEED = 10
MIN_SPEED = 5
MAX_SPEED = 20
POWER_UP_DURATION = 300  # Frames the power-up effect lasts

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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
        color = BLUE if self.type == 'speed' else YELLOW
        pygame.draw.rect(screen, color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Xenzia")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.load_high_score()
        self.walls_on = True
        self.speed = DEFAULT_SPEED
        self.menu_state = "main"
        self.create_menu_buttons()
        self.power_up = None
        self.power_up_effect = None
        self.power_up_timer = 0

    def create_menu_buttons(self):
        self.start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 50, "Start Game", GREEN, WHITE)
        self.settings_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Settings", GRAY, WHITE)
        self.quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Quit", RED, WHITE)
        self.walls_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, "Walls: On", GREEN, WHITE)
        self.speed_up_button = Button(WIDTH // 2 + 50, HEIGHT // 2, 100, 50, "+", GREEN, WHITE)
        self.speed_down_button = Button(WIDTH // 2 - 150, HEIGHT // 2, 100, 50, "-", RED, WHITE)
        self.back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Back", GRAY, WHITE)

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.level = 1
        self.power_up = None
        self.power_up_effect = None
        self.power_up_timer = 0

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

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
                    return PowerUp(pos, random.choice(['speed', 'invincibility']))
        return None

    def move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if self.walls_on and self.power_up_effect != 'invincibility':
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                return False  # Game over
        else:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in self.snake and self.power_up_effect != 'invincibility':
            return False  # Game over

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.food = self.spawn_food()
            self.increase_difficulty()
            if not self.power_up:
                self.power_up = self.spawn_power_up()
        else:
            self.snake.pop()

        if self.power_up and new_head == self.power_up.position:
            self.activate_power_up()

        if self.power_up:
            self.power_up.timer -= 1
            if self.power_up.timer <= 0:
                self.power_up = None

        if self.power_up_effect:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up_effect = None
                self.speed = DEFAULT_SPEED  # Reset speed when power-up effect ends

        return True

    def activate_power_up(self):
        self.power_up_effect = self.power_up.type
        self.power_up_timer = POWER_UP_DURATION
        if self.power_up_effect == 'speed':
            self.speed = min(self.speed + 2, MAX_SPEED)
        self.power_up = None

    def increase_difficulty(self):
        if self.score % 5 == 0:
            self.level += 1
            self.speed = min(self.speed + 1, MAX_SPEED)

    def draw_game(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = GREEN if self.power_up_effect != 'invincibility' else (i * 10 % 256, i * 20 % 256, i * 30 % 256)
            pygame.draw.rect(self.screen, color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw food
        pygame.draw.rect(self.screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw power-up
        if self.power_up:
            self.power_up.draw(self.screen)

        # Draw walls if enabled
        if self.walls_on:
            pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 2)

        # Draw score and level
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        speed_text = self.font.render(f"Speed: {self.speed}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
        self.screen.blit(speed_text, (WIDTH - speed_text.get_width() - 10, 50))

        pygame.display.flip()

    def handle_menu(self, pos):
        if self.menu_state == "main":
            if self.start_button.is_clicked(pos):
                self.menu_state = "game"
                self.reset_game()
            elif self.settings_button.is_clicked(pos):
                self.menu_state = "settings"
            elif self.quit_button.is_clicked(pos):
                pygame.quit()
                sys.exit()
        elif self.menu_state == "settings":
            if self.walls_button.is_clicked(pos):
                self.walls_on = not self.walls_on
                self.walls_button.text = "Walls: On" if self.walls_on else "Walls: Off"
            elif self.speed_up_button.is_clicked(pos):
                self.speed = min(self.speed + 1, MAX_SPEED)
            elif self.speed_down_button.is_clicked(pos):
                self.speed = max(self.speed - 1, MIN_SPEED)
            elif self.back_button.is_clicked(pos):
                self.menu_state = "main"

    def draw_menu(self):
        self.screen.fill(BLACK)

        if self.menu_state == "main":
            self.start_button.draw(self.screen)
            self.settings_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        elif self.menu_state == "settings":
            self.walls_button.draw(self.screen)
            self.speed_up_button.draw(self.screen)
            self.speed_down_button.draw(self.screen)
            self.back_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_menu(pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.direction = RIGHT

            if self.menu_state == "game":
                if not self.move_snake():
                    self.menu_state = "main"  # Game over, go back to the menu
                self.draw_game()
            else:
                self.draw_menu()

            self.clock.tick(self.speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()