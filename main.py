import sys
from typing import Tuple

import pygame

pygame.init()

# Window
screen = pygame.display.set_mode((800, 800))
background = pygame.image.load("../asset/grass.jpg")
background = pygame.transform.scale(background, (1280, 1280))
pygame.display.set_caption("Pets Army")
clock = pygame.time.Clock()

# -------------------------------
# LOAD SPRITESHEETS
# -------------------------------
llama_sheet = pygame.image.load("../asset/llama_walk.png").convert_alpha()
cow_sheet = pygame.image.load("../asset/cow_walk.png").convert_alpha()

COLUMNS = 4
ROWS = 4

FRAME_W = llama_sheet.get_width() // COLUMNS
FRAME_H = llama_sheet.get_height() // ROWS


def cut_frames(sheet: pygame.Surface) -> list[pygame.Surface]:
    frames = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            rect = pygame.Rect(c * FRAME_W, r * FRAME_H, FRAME_W, FRAME_H)
            frame = sheet.subsurface(rect)
            frames.append(frame)
    return frames


llama_frames = cut_frames(llama_sheet)
cow_frames = cut_frames(cow_sheet)


# -------------------------------
# UNIT CLASS 🔥
# -------------------------------
class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, frames: list[pygame.Surface]):
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
        current_x, current_y = self.rect.center
        target_x, target_y = self.target_position

        # close enough
        if abs(target_x - current_x) < 5 and abs(target_y - current_y) < 5:
            return

        speed = 4
        if boosted:
            speed = 7  # right click = faster

        next_x = current_x + (speed if target_x > current_x else -speed)
        next_y = current_y + (speed if target_y > current_y else -speed)

        self.rect.center = (next_x, next_y)

    def set_target_position(self, position: Tuple[int, int]):
        self.target_position = position


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))


# MAKE UNITS
llama = Unit(300, 200, llama_frames)
cow = Unit(500, 300, cow_frames)
background_sprite = Background(0, 0, background)

units = pygame.sprite.Group(background_sprite, llama, cow)

selected_unit: Unit | None = None


# -------------------------------
# GAME LOOP 🔥
# -------------------------------
while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ESC to close
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # LEFT CLICK → select or move
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_on_unit = False
            for unit in units:
                if isinstance(unit, Unit):
                    if unit.rect.collidepoint(mouse_pos):
                        selected_unit = unit
                        clicked_on_unit = True
                        break

            if not clicked_on_unit and selected_unit:
                selected_unit.set_target_position(mouse_pos)

    # -------------------------
    # KEYBOARD MOVEMENT (WASD)
    # -------------------------
    keys = pygame.key.get_pressed()
    move_speed = 4

    # right mouse = speed boost
    if pygame.mouse.get_pressed()[2]:
        move_speed = 7

    for unit in units:
        moving_with_keys = False
        if keys[pygame.K_w]:
            unit.rect.y += move_speed
            moving_with_keys = True
        if keys[pygame.K_s]:
            unit.rect.y -= move_speed
            moving_with_keys = True
        if keys[pygame.K_a]:
            unit.rect.x += move_speed
            moving_with_keys = True
        if keys[pygame.K_d]:
            unit.rect.x -= move_speed
            moving_with_keys = True
        if isinstance(unit, Unit) and moving_with_keys:
            unit.set_target_position(unit.rect.center)

    # UPDATE
    units.update()

    # DRAW
    screen.fill((0, 0, 0))
    units.draw(screen)

    # selection circle
    if selected_unit:
        pygame.draw.circle(screen, (0, 255, 0), selected_unit.rect.midbottom, 10, 2)

    pygame.display.flip()
    clock.tick(60)
