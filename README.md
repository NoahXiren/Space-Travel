# Space Walk

Space Walk is a thrilling space shooting game built using Pygame. Navigate your rocket through an asteroid field, shoot down asteroids, and aim for a high score. This README provides instructions for setting up, running, and understanding the game.

## Table of Contents

- [Gameplay](#gameplay)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Dependencies](#dependencies)
- [Game Structure](#game-structure)
- [Controls](#controls)
- [Assets](#assets)
- [License](#license)

## Gameplay

In Space Walk, you control a rocket that must avoid and destroy asteroids. The objective is to survive as long as possible while achieving the highest score. Points are scored based on the time survived. Shoot down asteroids using your laser to stay alive.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/space-walk.git
   cd space-walk
   ```

2. **Install the required dependencies:**
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure you have Pygame installed:**
   If not already included in your `requirements.txt`, install Pygame using:
   ```bash
   pip install pygame-ce
   ```

## Running the Game

To start the game, simply run the `main.py` script:
```bash
python main.py
```

## Dependencies

- **Python 3.x**
- **Pygame**: Used for game development, including graphics and sound.(community edition)

## Game Structure

### Main Components

- **Player**: The rocket the player controls. It can move up and down and shoot lasers.
- **Stars**: Background elements for a space effect.
- **Laser**: Projectiles shot by the player to destroy asteroids.
- **Asteroids**: Obstacles that move towards the player. They must be destroyed or avoided.
- **Explosion**: Animation played when an asteroid is destroyed.

### Key Classes and Functions

- **Player**:
  - Manages player movement and laser shooting.
  - `update()`: Updates player position and handles laser shooting.
  - `laser_timer()`: Manages laser cooldown.
- **Stars**: Static background elements.
- **Laser**: Handles laser movement and removal when off-screen.
- **Asteroids**: Manages asteroid movement, rotation, and destruction.
- **Explosion**: Manages explosion animation on asteroid destruction.
- **Collision()**: Detects collisions between player, lasers, and asteroids.
- **Display_score()**: Displays the player's current score based on survival time.

## Controls

- **Arrow Keys**: Move the rocket up and down.
- **Space Bar**: Shoot lasers.

## Assets

- **Images**:
  - Rocket, laser, star, asteroid, and explosion frames are located in the `Images` directory.
- **Sounds**:
  - Laser, explosion, and dead sounds are located in the `sounds` directory.

Ensure all assets are correctly placed in the respective directories:

```
space-walk/
│
├── Images/
│   ├── rocket.png
│   ├── laser.png
│   ├── star.png
│   ├── Aass.png
│   └── Explosion/
│       ├── 0.png
│       ├── 1.png
│       ├── 2.png
│       ├── 3.png
│       ├── 4.png
│       ├── 5.png
│       ├── 6.png
│       └── 7.png
│
├── sounds/
│   ├── laser_shoot.wav
│   ├── explosion.wav
│   └── dead.wav
│
├── font/
│   └── pixelify_sans.ttf
│
├── main.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
