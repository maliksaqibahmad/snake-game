# Snake Xenzia Game

**Snake Xenzia Game** is a modern remake of the classic Snake game, developed using Python and Pygame. This version introduces various new features such as power-ups, adjustable speed, and customizable settings to enhance gameplay.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Game Preview](#game-preview)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Settings](#settings)
- [Power-Ups](#power-ups)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [License](#license)

## Overview

This project is a customizable version of the famous Snake game, where the player controls a snake to consume food, grow longer, and avoid obstacles. As the game progresses, the difficulty increases, and power-ups can be collected to provide temporary advantages. The game includes a high score system and settings to adjust gameplay features like speed and wall collisions.

## Features

- **Classic Gameplay**: A modern take on the well-known Snake game.
- **Power-Ups**: Speed boost and invincibility to enhance the gameplay experience.
- **High Score System**: Your highest score is saved and displayed in-game.
- **Customizable Settings**: Toggle walls, adjust speed, and more.
- **Responsive Menu**: Start the game, adjust settings, or quit via a sleek menu interface.
- **Progressive Difficulty**: As your score increases, so does the challenge.

## Game Preview

![Game Screenshot](screenshot/screenshot.png)

## Installation

### Prerequisites

Make sure you have Python 3.x and the Pygame library installed:

1. Install Python 3 from the [official website](https://www.python.org/downloads/).
2. Install Pygame using pip:

   ```bash
   pip install pygame
   ```

### Clone the Repository

To get started, clone the repository and navigate to the project folder:

```bash
git clone https://github.com/maliksaqibahmad/snake-game.git
cd snake-game
```

### Run the Game

After cloning the repository, run the game by executing the following command:

```bash
python snake.py
```

## How to Play

- Use the **arrow keys** to control the snake (Up, Down, Left, Right).
- The goal is to eat the food (red squares) and grow the snake longer.
- Avoid running into the walls or your own body.
- Collect power-ups for temporary boosts.

### Controls

- **Arrow Keys**: Control snake's movement.
- **ESC**: Return to the main menu during gameplay.

### Scoring

- Every time you eat a piece of food, your score increases by 1.
- Your current score and high score will be displayed on the game screen.

## Settings

You can customize the game through the settings menu, accessible from the main menu.

### Adjustable Options

- **Toggle Walls**: Turn wall collisions on or off. If turned off, the snake will wrap around the screen edges.
- **Speed**: Adjust the game speed, with a range from 5 (slow) to 20 (fast).

## Power-Ups

During gameplay, you'll encounter random power-ups that give you temporary benefits:

- **Speed Boost (Blue)**: Increases your snake's speed.
- **Invincibility (Yellow)**: Makes your snake immune to walls and its own body for a short period.

Power-ups spawn with a 10% chance after consuming food and last for a limited number of frames.

## Contributors

Thanks to these wonderful people who have contributed to the project:

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## Contributing

Contributions are welcome! If you'd like to enhance the game, feel free to fork the repository and submit a pull request.

### How to Contribute

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes.
4. Commit and push your changes:

   ```bash
   git commit -m "Add feature"
   git push origin feature/your-feature-name
   ```

5. Open a pull request for review.

Possible areas for contributions:

- Add more power-ups (e.g., slow motion, double points).
- Improve the visual design and sound effects.
- Implement additional levels or snake skins.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
