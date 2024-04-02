import os
import time
import math

width, height = 70, 20  # Width and height of the animation
wave_length, wave_height = 20, 5  # Length and height of the waves

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]  # Color cycle

def draw_wave(offset):
    for y in range(height):
        line = ""
        for x in range(width):
            y_value_top = wave_height * math.sin((x + offset) * 2 * math.pi / wave_length) + (height / 4)
            y_value_bottom = -wave_height * math.sin((x + offset) * 2 * math.pi / wave_length) + (3 * height / 4)
            color = colors[(x + offset) // wave_length % len(colors)]  # Cycle through colors

            if y == round(y_value_top) or y == round(y_value_bottom):
                if width // 2 - 2 < x < width // 2 + 3 and y == height // 2:  # Position for "JHANA"
                    line += "JHANA"[x - (width // 2 - 2)]
                else:
                    line += color + "*" + RESET
            else:
                line += " "
        print(line)

def animate_wave(steps, delay):
    for offset in range(steps):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        draw_wave(offset)
        time.sleep(delay)

steps = 70  # Number of frames in the animation
delay = 0.1  # Delay in seconds between each frame

animate_wave(steps, delay)
