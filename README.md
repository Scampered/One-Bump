# One Bump

A Doodle Jump-style endless platformer built with **Python** and **Pygame**. Bounce from platform to platform, climb as high as you can, and beat your own high score and altitude record.

Built as a school project in 2025 — entered into the school's **ScienTIA** contest, where it placed **2nd**. Mainly built by following a tutorial, with help from ChatGPT for debugging along the way.

## Gameplay

- Move left/right with **A/D** or the arrow keys.
- Land on platforms to automatically bounce upward — miss them all and fall off the bottom of the screen to end the run.
- Some platforms drift left and right; the higher you climb, the faster and wider they move.
- Score increases as platforms scroll past and despawn below the screen.
- Altitude tracks the highest point you've reached in the run.
- Your best score and altitude are saved locally (`score.txt`, `altitude.txt`) and shown in-game as a "high score line" to beat.
- Press **SPACE** to restart after a run ends.

## Features

- Procedurally generated platforms with randomized size, position, and movement
- Difficulty scales with altitude — platform speed and movement range increase the higher you climb
- Parallax-style infinite scrolling background
- Persistent high score / top altitude tracking across sessions
- Sound effects (jump, death) and background music

## Running it

```bash
pip install pygame
python main.py
```

## Project structure

```
One Bump/
├── main.py       # game entry point — core loop, Player and Platform classes
├── menu.py       # earlier/alternate version of the game loop
├── assets/       # sprites, fonts, and audio
├── score.txt     # persisted high score
└── altitude.txt  # persisted top altitude
```
