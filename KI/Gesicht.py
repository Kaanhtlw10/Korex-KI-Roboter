import pygame
import sys

# Pygame initialisieren
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesicht vom Korex")

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
clock = pygame.time.Clock()

# Funktionen für verschiedene Gesichtsausdrücke
def draw_face(expression="neutral"):
    screen.fill(BLACK)

    if expression == "neutral":
        # Normale Augen
        pygame.draw.rect(screen, CYAN, (220, 250, 90, 80))
        pygame.draw.rect(screen, CYAN, (490, 250, 90, 80))
        # Neutrale Augenbrauen (waagerecht)
        pygame.draw.line(screen, CYAN, (210, 175), (320, 165), 12)
        pygame.draw.line(screen, CYAN, (480, 165), (590, 175), 12)
        # Gerader Mund
        pygame.draw.rect(screen, CYAN, (300, 420, 200, 40))

    elif expression == "happy":
        # Glückliche Augen (z.B. kleinere Quadrate oder hochgezogen)
        pygame.draw.rect(screen, CYAN, (220, 220, 90, 90))
        pygame.draw.rect(screen, CYAN, (490, 220, 90, 90))
        # Augenbrauen schräg
        pygame.draw.line(screen, CYAN, (210, 190), (320, 170), 12)
        pygame.draw.line(screen, CYAN, (480, 170), (590, 190), 12)
        # Breiter, grinsender Mund (oder ein dickes Lächeln)
        pygame.draw.rect(screen, CYAN, (280, 410, 240, 60))

    elif expression == "blink":
        # Geschlossene Augen (nur ein Strich)
        pygame.draw.line(screen, CYAN, (220, 260), (310, 260), 12)
        pygame.draw.line(screen, CYAN, (490, 260), (580, 260), 12)
        # Augenbrauen normal
        pygame.draw.line(screen, CYAN, (210, 175), (320, 165), 12)
        pygame.draw.line(screen, CYAN, (480, 165), (590, 175), 12)
        # Mund
        pygame.draw.rect(screen, CYAN, (300, 420, 200, 20))

# Aktueller Gesichtsausdruck
current_expression = "neutral"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Tastensteuerung zum Testen der Ausdrücke:
            elif event.key == pygame.K_1:
                current_expression = "neutral"
            elif event.key == pygame.K_2:
                current_expression = "happy"
            elif event.key == pygame.K_3:
                current_expression = "blink"

    # Gesicht mit dem aktuellen Zustand zeichnen
    draw_face(current_expression)

    pygame.display.flip()
    clock.tick(60)