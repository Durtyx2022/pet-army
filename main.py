import pygame
import sys

pygame.init()

# Window
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# Load the spritesheet
spritesheet = pygame.image.load("../asset/llama_walk.png").convert_alpha()

# --- SPRITESHEET INFO ---
# Your sheet is 4 columns × 4 rows = 16 frames total
COLUMNS = 4
ROWS = 4
FRAME_WIDTH = spritesheet.get_width() // COLUMNS
FRAME_HEIGHT = spritesheet.get_height() // ROWS

# Extract animation frames
frames = []
for row in range(ROWS):
    for col in range(COLUMNS):
        frame_rect = pygame.Rect(
            col * FRAME_WIDTH,
            row * FRAME_HEIGHT,
            FRAME_WIDTH,
            FRAME_HEIGHT,
        )
        frame = spritesheet.subsurface(frame_rect)
        frames.append(frame)


class Llama(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1

    def update(self):
        self.index += self.animation_speed
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]


# Create a llama sprite
llama = Llama(200, 150, frames=frames[4:8])
all_sprites = pygame.sprite.Group(llama)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
