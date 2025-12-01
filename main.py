import sys
from typing import Tuple
import pygame

pygame.init()

# -------------------------------
# WINDOW + CLOCK
# -------------------------------
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pets Army")
clock = pygame.time.Clock()

# -------------------------------
# LOAD BACKGROUND
# -------------------------------
background = pygame.image.load("../asset/grass.jpg")
background = pygame.transform.scale(background, (1280, 1280))

# -------------------------------
# CAMERA
# -------------------------------
camera_x = 0
camera_y = 0
camera_target_x = 0
camera_target_y = 0
CAMERA_SPEED = 15  # cinematic smoothness

# -------------------------------
# DOUBLE CLICK DETECTION
# -------------------------------
last_click_time = 0
DOUBLE_CLICK_DELAY = 300  # ms

# -------------------------------
# LOAD SPRITESHEETS
# -------------------------------
llama_sheet = pygame.image.load("../asset/llama_walk.png").convert_alpha()
cow_sheet = pygame.image.load("../asset/cow_walk.png").convert_alpha()

COLUMNS = 4
ROWS = 4
FRAME_W = llama_sheet.get_width() // COLUMNS
FRAME_H = llama_sheet.get_height() // ROWS

def cut_frames(sheet):
    frames = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            rect = pygame.Rect(c * FRAME_W, r * FRAME_H, FRAME_W, FRAME_H)
            frames.append(sheet.subsurface(rect))
    return frames

llama_frames = cut_frames(llama_sheet)
cow_frames = cut_frames(cow_sheet)

# -------------------------------
# UNIT CLASS
# -------------------------------
class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames[4:8]  # walking cycle
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.target_position = (x, y)
        self.animation_speed = 0.1

    def update(self):
        right_click = pygame.mouse.get_pressed()[2]

        # animation boost
        if right_click:
            self.index += self.animation_speed * 2
        else:
            self.index += self.animation_speed

        if self.index >= len(self.frames):
            self.index = 0

        self.image = self.frames[int(self.index)]
        self.move_towards_target(right_click)

    def move_towards_target(self, boosted):
        x, y = self.rect.center
        tx, ty = self.target_position

        if abs(tx - x) < 5 and abs(ty - y) < 5:
            return

        speed = 7 if boosted else 4
        x += speed if tx > x else -speed
        y += speed if ty > y else -speed

        self.rect.center = (x, y)

    def set_target_position(self, pos: Tuple[int, int]):
        self.target_position = pos

# -------------------------------
# BACKGROUND SPRITE
# -------------------------------
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=(x, y))

background_sprite = Background(0, 0, background)

# -------------------------------
# CREATE UNITS
# -------------------------------
llama = Unit(300, 200, llama_frames)
cow = Unit(500, 300, cow_frames)

units = pygame.sprite.Group(background_sprite, llama, cow)
selected_unit: Unit | None = None

# -------------------------------
# GAME LOOP
# -------------------------------
while True:
    mouse_pos = pygame.mouse.get_pos()
    world_mouse = (mouse_pos[0] - camera_x, mouse_pos[1] - camera_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # ---------------------------
        # LEFT CLICK SELECTION + DOUBLE CLICK
        # ---------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            double_click = (now - last_click_time) < DOUBLE_CLICK_DELAY
            last_click_time = now

            clicked_unit = None
            for unit in [u for u in units if isinstance(u, Unit)]:
                if unit.rect.collidepoint(world_mouse):
                    clicked_unit = unit
                    break

            # CLICKED ON UNIT
            if clicked_unit:
                selected_unit = clicked_unit

                # DOUBLE CLICK → move camera smoothly to center on unit
                if double_click:
                    camera_target_x = -selected_unit.rect.centerx + WIDTH // 2
                    camera_target_y = -selected_unit.rect.centery + HEIGHT // 2

            # CLICKED EMPTY SPACE → move selected unit
            else:
                if selected_unit:
                    selected_unit.set_target_position(world_mouse)

    # ---------------------------
    # KEYBOARD MOVEMENT
    # ---------------------------
    keys = pygame.key.get_pressed()
    move_speed = 7 if pygame.mouse.get_pressed()[2] else 4

    if selected_unit:
        moving = False
        if keys[pygame.K_w]:
            selected_unit.rect.y -= move_speed
            moving = True
        if keys[pygame.K_s]:
            selected_unit.rect.y += move_speed
            moving = True
        if keys[pygame.K_a]:
            selected_unit.rect.x -= move_speed
            moving = True
        if keys[pygame.K_d]:
            selected_unit.rect.x += move_speed
            moving = True

        if moving:
            selected_unit.set_target_position(selected_unit.rect.center)

        # ---------------------------
        # CAMERA FOLLOW BORDER (CINEMATIC)
        # ---------------------------
        sx, sy = selected_unit.rect.center

        # LEFT/RIGHT
        if sx + camera_x < 200:
            camera_target_x += 10
        if sx + camera_x > WIDTH - 200:
            camera_target_x -= 10

        # TOP/BOTTOM
        if sy + camera_y < 200:
            camera_target_y += 10
        if sy + camera_y > HEIGHT - 200:
            camera_target_y -= 10

    # ---------------------------
    # SMOOTH CAMERA MOVE (CINEMATIC)
    # ---------------------------
    camera_x += (camera_target_x - camera_x) / CAMERA_SPEED
    camera_y += (camera_target_y - camera_y) / CAMERA_SPEED

    # ---------------------------
    # UPDATE UNITS
    # ---------------------------
    units.update()

    # ---------------------------
    # DRAW EVERYTHING WITH CAMERA OFFSET
    # ---------------------------
    screen.fill((0, 0, 0))
    for sprite in units:
        screen.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

    # DRAW SELECTION CIRCLE
    if selected_unit:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (selected_unit.rect.midbottom[0] + camera_x,
             selected_unit.rect.midbottom[1] + camera_y),
            10, 2
        )

    pygame.display.flip()
    clock.tick(60)
