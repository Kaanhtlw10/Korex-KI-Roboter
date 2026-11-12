import random
import sys

import pygame

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

screen = None
clock = None

# --- Animations-Variablen ---
# Zeitgeber für automatisches Blinzeln
last_blink_time = 0
next_blink_interval = random.randint(2000, 5000)  # Blinzelt alle 2 bis 5 Sekunden
is_blinking = False
blink_start_time = 0

# Zeitgeber für das Herumschauen
last_gaze_time = 0
gaze_offset_x = 0  # Verschiebung der Pupillen (-20 bis +20)
gaze_offset_y = 0


def initialize_pygame():
    global screen, clock, last_blink_time, last_gaze_time

    if not pygame.get_init():
        pygame.init()

    if screen is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Korex")

    if clock is None:
        clock = pygame.time.Clock()

    if last_blink_time == 0:
        last_blink_time = pygame.time.get_ticks()

    if last_gaze_time == 0:
        last_gaze_time = pygame.time.get_ticks()


def update_animations():
    global last_blink_time, next_blink_interval, is_blinking, blink_start_time
    global last_gaze_time, gaze_offset_x, gaze_offset_y

    if not pygame.get_init() or screen is None:
        return

    current_time = pygame.time.get_ticks()

    # 1. Automatisches Blinzeln steuern
    if not is_blinking and (current_time - last_blink_time > next_blink_interval):
        is_blinking = True
        blink_start_time = current_time

    # Wenn er blinzelt, soll das nur 150 Millisekunden dauern
    if is_blinking and (current_time - blink_start_time > 150):
        is_blinking = False
        last_blink_time = current_time
        next_blink_interval = random.randint(2000, 5000)  # Nächsten Blinzel-Zeitpunkt neu losen

    # 2. Ab und zu in eine andere Richtung schauen (alle 3-6 Sekunden)
    if current_time - last_gaze_time > random.randint(3000, 6000):
        # Zufällige Blickrichtung wählen (links, rechts, oben, unten oder geradeaus)
        gaze_offset_x = random.choice([-25, 0, 25])
        gaze_offset_y = random.choice([-15, 0, 15])
        last_gaze_time = current_time


def draw_face():
    if screen is None:
        return

    screen.fill(BLACK)

    # Basis-Positionen der Augen
    left_eye_center = (270, 250)
    right_eye_center = (530, 250)

    if is_blinking:
        # Wenn er blinzelt: Nur horizontale Striche statt runder Augen
        pygame.draw.line(screen, CYAN, (215, 250), (325, 250), 12)
        pygame.draw.line(screen, CYAN, (475, 250), (585, 250), 12)

        # Augenbrauen leicht nach unten beim Blinzeln
        pygame.draw.line(screen, CYAN, (210, 175), (320, 165), 12)
        pygame.draw.line(screen, CYAN, (480, 165), (590, 175), 12)
    else:
        # Normale offene Augen (Äußerer Kreis)
        pygame.draw.circle(screen, CYAN, left_eye_center, 55)
        pygame.draw.circle(screen, CYAN, right_eye_center, 55)

        # Pupillen, die sich je nach Blickrichtung (gaze_offset) bewegen
        pupil_left = (left_eye_center[0] + gaze_offset_x, left_eye_center[1] + gaze_offset_y)
        pupil_right = (right_eye_center[0] + gaze_offset_x, right_eye_center[1] + gaze_offset_y)

        # Schwarze Pupillen zeichnen (damit man sieht, wohin er schaut)
        pygame.draw.circle(screen, BLACK, pupil_left, 20)
        pygame.draw.circle(screen, BLACK, pupil_right, 20)

        # Dynamische Augenbrauen (leicht geneigt je nach Blick)
        brow_tilt = gaze_offset_y // 2  # Augenbrauen bewegen sich leicht mit
        pygame.draw.line(screen, CYAN, (210, 175 + brow_tilt), (320, 165 + brow_tilt), 12)
        pygame.draw.line(screen, CYAN, (480, 165 + brow_tilt), (590, 175 + brow_tilt), 12)

    # Mund – freundlich, sauber und leicht lächelnd
    mouth_points = [(280, 410), (340, 440), (400, 455), (460, 440), (520, 410)]
    pygame.draw.lines(screen, CYAN, False, mouth_points, 12)


def main():
    initialize_pygame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Berechne die Animationen (Timer, Blickrichtung etc.)
        update_animations()

        # Zeichne das Gesicht auf Basis der aktuellen Werte
        draw_face()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()