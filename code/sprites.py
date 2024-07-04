import pygame
from settings import *
from random import choice, randint

main_file_dir = ".."

# Background class
class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups) # call superclass constructor
        bg_image = pygame.image.load(main_file_dir + '/graphics/environment/background.png').convert()

        full_height = scale_factor * bg_image.get_height()
        full_width = scale_factor * bg_image.get_width()
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        # create a big image that is twice the size of original image for seamless scrolling
        self.image = pygame.Surface((full_width * 2, full_height)) # create a surface that is twice as wide as the full_sized_image
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))
        self.rect = self.image.get_rect(topleft = (0, 0)) # get the rectangle of the scaled image, position its top left at (0, 0)
        self.pos = pygame.math.Vector2(self.rect.topleft) # set initial position to be the top left of self.rect (which is (0, 0))

    def update(self, dt):
        self.pos.x -= BACKGROUND_SPEED * dt # background moves left horizontally
        if self.rect.centerx <= 0: # if original sized bg image out of screen
            self.pos.x = 0
        self.rect.x = round(self.pos.x) # update the x position of bg image

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        ground_surf = pygame.image.load(main_file_dir + '/graphics/environment/ground.png').convert_alpha() # convert alpha to preserve transparency
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor) # Vector2 can be implicitly converted to a tuple
        
        # position
        self.rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT)) # note that the ground image has already been doubled when importing
        self.pos = pygame.Vector2(self.rect.topleft)

        # mask: a mask in pygame is a tool used for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # ground speed
        self.speed = GROUND_SPEED

        # type
        self.type = 'ground'
    
    def update(self, dt):
        self.pos.x -= self.speed * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = GRAVITY # acceleration
        self.direction = 0 # velocity

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.jump_sound = pygame.mixer.Sound(main_file_dir + '/sounds/jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(main_file_dir + f'/graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -JUMP_HEIGHT # give the plane an upward velocity

    def animate(self, dt):
        self.frame_index += 15 * dt # adjust the speed of the plane animation
        self.image = self.frames[int(self.frame_index) % 3]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.07, 1) # 3 args: image, rotation angle, scale. We set rotation angle to be propotional to the velocity of the plane
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image) # create a rotated mask

    def update(self, dt):
        # the below order matters because animate fetches a new image each time it is called
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate() # rotate is the last because it 

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor, speed):
        super().__init__(groups)

        random_num = randint(1, 6)
        # 1/3 chance of spawning a stone, 2/3 chance of spawning a pillar
        if random_num <= 4: # spawn a pillar
            orientation = choice(('up', 'down')) # randomly chooses up or down
            surf = pygame.image.load(main_file_dir + f'/graphics/obstacles/{choice(tuple(i for i in range(4)))}.png').convert_alpha()
            self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)

            x = WINDOW_WIDTH + 70 # x position of the obstacle is outside of the window at first

            if orientation == 'up':
                y = WINDOW_HEIGHT + randint(10, 50)
                self.rect = self.image.get_rect(midbottom = (x, y))
            else:
                y = -randint(10, 50)
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect = self.image.get_rect(midtop = (x, y))

        else: # spawn a stone
            surf = pygame.image.load(main_file_dir + f'/graphics/obstacles/4.png').convert_alpha()
            self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor * 0.8)
            self.rect = self.image.get_rect(center = (WINDOW_WIDTH + 90, WINDOW_HEIGHT / 2 + randint(-50, 50)))

        self.speed = speed
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # type
        self.type = 'obstacle'

    def update(self, dt):
        self.pos.x -= self.speed * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100: # destroy the obstacle once it is out of the screen
            self.kill()
