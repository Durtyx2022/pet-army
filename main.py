import pygame
import sys

pygame.init()

# Window
screen = pygame.display.set_mode((600, 400))
background = pygame.image.load("../asset/grass.jpg")
clock = pygame.time.Clock()

# -------------------------------
# LOAD BOTH SPRITESHEETS 🔥
# -------------------------------
llama_sheet = pygame.image.load("../asset/llama_walk.png").convert_alpha()
cow_sheet   = pygame.image.load("../asset/cow_walk.png").convert_alpha()

COLUMNS = 4
ROWS = 4

FRAME_W = llama_sheet.get_width() // COLUMNS
FRAME_H = llama_sheet.get_height() // ROWS


# FRAME CUTTING FUNCTION
def cut_frames(sheet):
    frames = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            rect = pygame.Rect(c * FRAME_W, r * FRAME_H, FRAME_W, FRAME_H)
            frame = sheet.subsurface(rect)
            frames.append(frame)
    return frames


llama_frames = cut_frames(llama_sheet)
cow_frames   = cut_frames(cow_sheet)


# -------------------------------
# SPRITE CLASSES 🔥
# -------------------------------
class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames[4:8]  # walking cycle
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.animation_speed = 0.1

    def update(self):
        # animation
        self.index += self.animation_speed
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]


# CREATE UNITS
llama = Unit(300, 200, llama_frames)
cow   = Unit(500, 300, cow_frames)

units = pygame.sprite.Group(llama, cow)

selected_unit = None


# -------------------------------
# GAME LOOP 🔥💯
# -------------------------------
while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 🖱️ LEFT CLICK = SELECT OR TELEPORT
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            clicked_on_unit = False

            # Check if click hits a unit
            for unit in units:
                if unit.rect.collidepoint(mouse_pos):
                    selected_unit = unit
                    clicked_on_unit = True
                    break

            # If click NOT on a unit → teleport selected one
            if not clicked_on_unit and selected_unit != None:
                selected_unit.rect.center = mouse_pos

    # update animation
    units.update()

    # DRAW
    screen.blit(background, (0, 0))
    units.draw(screen)

    # Draw selection circle 🟢
    if selected_unit:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            selected_unit.rect.midbottom,
            10,
            2
        )

    pygame.display.flip()
    clock.tick(60)
