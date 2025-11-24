import pygame
import sys

pygame.init()

# Window
screen = pygame.display.set_mode((600, 400))
background = pygame.image.load("../asset/grass.jpg")
screen.blit(background, (0, 0))
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
llama = Llama(300, 200, frames=frames[4:8])
all_sprites = pygame.sprite.Group(llama)
last_move_time = 0  # stores the last time the sprite moved
move_interval = 2000 
# Game loop
timestamp = 0
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if current_time - last_move_time >= move_interval:
        llama.rect.x += 10  # move right by 10 pixels (adjust as needed)
        last_move_time = current_time
    screen.fill((0, 0, 0))  # clear screen
    screen.blit(background,(0,0))
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
