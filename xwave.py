import math
import os
import sys
import time
import select
import termios
import tty

# Color ANSI codes
COLOR_CYAN = "\033[1;36m"
COLOR_BLUE = "\033[0;34m"
COLOR_MAGENTA = "\033[1;35m"
COLOR_WHITE = "\033[1;37m"
COLOR_DIM = "\033[2;37m"
COLOR_RESET = "\033[0m"

CHARS_WAVE_PRIMARY = ['░', '▒', '▓', '█', '▓', '▒', '░']
CHARS_WAVE_SECONDARY = ['·', '∘', '•', '∘', '·']
BH_PARTICLES = ['@', '%', '#', '*', '+', '=', '-', ':', '.']

class RawTerminal:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        sys.stdout.write("\033[?25l\033[2J") # Hide cursor, clear screen
        sys.stdout.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        sys.stdout.write("\033[?25h\033[0m\033[2J\033[1;1H") # Show cursor, reset
        sys.stdout.flush()

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def render_black_hole():
    frame = 0
    while True:
        key = get_key()
        if key in ['q', '\x1b']:
            break

        cols, rows = os.get_terminal_size()
        center_x = cols // 2
        center_y = rows // 2
        buffer = ["\033[2J"]

        # Gravitational Lensing & Accretion Spiral
        for ring in range(3, 16):
            particle_count = ring * 6
            speed_multiplier = 2.5 / (ring ** 0.5) # Keplerian velocity profile
            
            for i in range(particle_count):
                angle = (i / particle_count) * (2 * math.pi) + (frame * 0.08 * speed_multiplier)
                
                # Elliptical distortion simulating tilted accretion disk
                x = int(center_x + math.cos(angle) * (ring * 2.2))
                y = int(center_y + math.sin(angle) * (ring * 0.8))

                if 1 <= x <= cols and 1 <= y <= rows:
                    char_idx = min(int((ring / 16) * len(BH_PARTICLES)), len(BH_PARTICLES) - 1)
                    symbol = BH_PARTICLES[char_idx]

                    if ring <= 5:
                        color = COLOR_MAGENTA # Hot inner region
                    elif ring <= 10:
                        color = COLOR_CYAN    # Mid disk
                    else:
                        color = COLOR_BLUE    # Fading outer edge

                    buffer.append(f"\033[{y};{x}H{color}{symbol}")

        # Singularity / Event Horizon Core
        core = "  (●)  "
        buffer.append(f"\033[{center_y};{center_x - 3}H{COLOR_WHITE}{core}{COLOR_RESET}")

        # Text Overlay
        msg = "alone in the universe....."
        msg_x = max(1, (cols - len(msg)) // 2)
        msg_y = max(1, rows - 2)
        buffer.append(f"\033[{msg_y};{msg_x}H{COLOR_DIM}{msg}{COLOR_RESET}")

        sys.stdout.write("".join(buffer))
        sys.stdout.flush()
        frame += 1
        time.sleep(0.04)

def main():
    phase1, phase2, phase3 = 0.0, 0.0, 0.0
    input_buffer = ""
    trigger = "fee1 d3ad"

    with RawTerminal():
        while True:
            key = get_key()
            if key:
                if key in ['q', '\x1b']:
                    break
                input_buffer += key
                if len(input_buffer) > 15:
                    input_buffer = input_buffer[-15:]
                if trigger in input_buffer:
                    input_buffer = ""
                    render_black_hole()

            cols, rows = os.get_terminal_size()
            center_y = rows / 2.0
            buffer = ["\033[2J"]

            for x in range(1, cols + 1):
                x_f = float(x)

                # Wave Superposition Math Equation:
                # y(x, t) = A1*sin(k1*x + w1*t) + A2*cos(k2*x - w2*t) + A3*sin(k3*x + w3*t)
                y1 = center_y + (math.sin(x_f * 0.07 + phase1) * (center_y * 0.45)) + (math.cos(x_f * 0.03 + phase2) * (center_y * 0.2))
                y2 = center_y + (math.cos(x_f * 0.11 - phase2) * (center_y * 0.3))
                y3 = center_y + (math.sin(x_f * 0.04 + phase3) * (center_y * 0.6))

                r1 = max(1, min(rows, int(y1)))
                r2 = max(1, min(rows, int(y2)))
                r3 = max(1, min(rows, int(y3)))

                # Primary Deep Wave Layer
                idx1 = int((y1 / rows) * len(CHARS_WAVE_PRIMARY)) % len(CHARS_WAVE_PRIMARY)
                buffer.append(f"\033[{r1};{x}H{COLOR_CYAN}{CHARS_WAVE_PRIMARY[idx1]}")

                # Secondary Interference Layer
                idx2 = int((y2 / rows) * len(CHARS_WAVE_SECONDARY)) % len(CHARS_WAVE_SECONDARY)
                buffer.append(f"\033[{r2};{x}H{COLOR_BLUE}{CHARS_WAVE_SECONDARY[idx2]}")

                # Crest Peak
                buffer.append(f"\033[{r3};{x}H{COLOR_WHITE}█")

            sys.stdout.write("".join(buffer))
            sys.stdout.flush()

            phase1 += 0.12
            phase2 += 0.07
            phase3 += 0.18
            time.sleep(0.03)

if __name__ == "__main__":
    main()
