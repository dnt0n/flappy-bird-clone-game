import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

main_file_dir = ".."

class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load(main_file_dir + '/graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # current difficulty
        self.difficulty = 0

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        self.ground = Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 2) # adjust plane size here

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1 # create custom event obstacle_timer
        pygame.time.set_timer(self.obstacle_timer, int(OBSTACLE_INTERVAL / GAME_SPEED_FACTORS[self.difficulty])) # run this event every 1000ms
        self.spawn_obstacles = True

        # text
        self.font = pygame.font.Font(main_file_dir + '/graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load(main_file_dir + '/graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # music
        self.bg_music = pygame.mixer.Sound(main_file_dir + '/sounds/music.wav')
        self.bg_music.set_volume(0.3)
        self.bg_music.play(loops = -1) # set loops to -1 so it doesn't stop playing

        self.crash_sound = pygame.mixer.Sound(main_file_dir + '/sounds/crash.wav')
        self.crash_sound.set_volume(0.6)
    
    def collisions(self):
        # takes in 3 parameters: target sprite, collision sprite groups, kill boolean (True means destroy the target sprite) 
        # return a list of collision sprites that collided with the target sprites, if no collision, list will be empty
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) \
            or self.plane.rect.top <= 0: # if the plane touches the top
            for sprite in self.collision_sprites:
                sprite.kill() # destroy all the collision sprites (ground and obstacles)
            self.active = False
            self.plane.kill() # destroy the plane after collision
            self.crash_sound.play()
    
    def display_score(self):
        if self.active:
            self.score = abs(pygame.time.get_ticks() - self.start_offset) // 1000 # time.get_ticks() gives the time since the programme started in ms
            score_y = WINDOW_HEIGHT / 10
        else:
            score_y = WINDOW_HEIGHT / 2 + self.menu_rect.height

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, score_y))
        self.display_surface.blit(score_surf, score_rect)
    
    def update_difficulty(self):
        # make the game increasingly difficult
        # easy mode
        if self.score <= 15:
            self.difficulty = 0

        # transition
        elif 16 <= self.score == 18 and self.active:
            self.spawn_obstacles = False
            self.difficulty = 1
            self.ground.speed = GROUND_SPEED * GAME_SPEED_FACTORS[self.difficulty]
            pygame.time.set_timer(self.obstacle_timer, int(OBSTACLE_INTERVAL / 1.2))

            faster_surf = self.font.render("Faster!!!", True, 'black')
            faster_rect = faster_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.display_surface.blit(faster_surf, faster_rect)

        # medium mode
        elif 19 <= self.score <= 32:
            self.spawn_obstacles = True
        
        # transition
        elif 33 <= self.score == 35 and self.active:
            self.spawn_obstacles = False
            self.difficulty = 2
            self.ground.speed = GROUND_SPEED * GAME_SPEED_FACTORS[self.difficulty]
            pygame.time.set_timer(self.obstacle_timer, int(OBSTACLE_INTERVAL / 1.4))  

            faster_surf = self.font.render("Even Faster!!!!!!", True, 'black')
            faster_rect = faster_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.display_surface.blit(faster_surf, faster_rect)

        # hard mode
        elif self.score >= 36:
            self.spawn_obstacles = True

    def run(self): 
        last_time = time.time()
        while True: # for every frame

            # delta time for frame rate-independent update
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 2)
                        self.ground = Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
                        self.start_offset = pygame.time.get_ticks()
                        self.active = True

                if event.type == self.obstacle_timer and self.active and self.spawn_obstacles: # spawn obstacle in some interval when the game is active
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * OBSTACLE_SCALE_FACTOR, OBSTACLE_SPEED * GAME_SPEED_FACTORS[self.difficulty])

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt) # call the update method of all sprites
            self.all_sprites.draw(self.display_surface) # draw all sprites on display surface
            self.display_score() # draw the score on the display surface
            self.update_difficulty() # update the difficulty
            
            if self.active: # if game is active
                self.collisions()
            else: # if game is not active (game over)
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()
