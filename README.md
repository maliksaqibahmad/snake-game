# Snake Game

Snake Game is a modernized version of the classic Snake game, built using Python and Pygame. It features multiple enhancements, including speed adjustments, difficulty levels, power-ups, and a settings menu for customization.

## Table of Contents

- Features
- Requirements
- Installation
- Usage
- Gameplay
- Power-Ups
- Settings
- Contributing
- License

## Features

- Classic Snake Gameplay: Navigate the snake to eat food and grow longer without colliding with walls or itself.
- Power-Ups: Collect special power-ups like speed boosts and invincibility.
- Difficulty Levels: As your score increases, the game becomes progressively harder.
- Customizable Settings: Adjust speed, toggle wall collisions, and more.
- High Score Tracking: The game saves and displays your highest score.
- Responsive Menu: Start the game, adjust settings, and quit from an intuitive menu.

## Requirements

To run this game, you'll need the following:

- Python 3.x
- Pygame library

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/maliksaqibahmad/snake-game.git
    cd snake-game
    ```

2. Install the required dependencies:
    ```
    pip install pygame
    ```

## Usage

To start the game, run the script:

```
python snake.py
```

Once the game starts, you can navigate the main menu to start the game, adjust settings, or quit.

## Gameplay

- Controls: 
  - Use the arrow keys to control the snake's movement (Up, Down, Left, Right).
  - Try to eat the red food to grow longer and score points.
  - Avoid running into the walls (if walls are enabled) or yourself.
  - The game ends if you crash into a wall or yourself.

- Scoring: 
  - Each piece of food increases your score by 1 point.
  - Your score and the high score are displayed on the screen.

- Game Over: 
  - The game will return to the main menu after the game is over.

## Power-Ups

Occasionally, special power-ups appear on the screen, indicated by different colors:

- Speed Boost (Blue): Increases the snake's speed for a limited time.
- Invincibility (Yellow): Makes the snake immune to collisions for a short duration.

## Settings

The game includes a settings menu where you can adjust the following:

- Toggle Walls: Enable or disable wall collisions (default is ON).
- Adjust Speed: Increase or decrease the snake's movement speed (range from 5 to 20).

To access the settings:

1. Select "Settings" from the main menu.
2. Use the buttons to toggle walls or adjust speed.
3. Press "Back" to return to the main menu.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```
    git checkout -b feature/your-feature-name
    ```
3. Make your changes.
4. Commit your changes:
    ```
    git commit -m "Add feature or fix description"
    ```
5. Push to the branch:
    ```
    git push origin feature/your-feature-name
    ```
6. Open a pull request.

### Ideas for Contributions

- Add more power-ups (e.g., slow motion, double score).
- Improve visuals and add sound effects.
- Create additional levels or themes.
- Implement multiplayer mode.
