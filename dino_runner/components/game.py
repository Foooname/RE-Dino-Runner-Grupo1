import pygame

from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacles.obstacles_manager import ObstacleManager
from dino_runner.components.powerups.power_up_manager import PowerUpManager
from dino_runner.components.powerups.shield import Shield
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, DEFAULT_TYPE, SCREEN_WIDTH, SMALL_CACTUS, TITLE, FPS,RUNNING, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        pygame.mixer.music.load('dino_runner/assets/music.mp3')

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_ups_manager = PowerUpManager()
        self.death_count = 0
        self.score = Score()
        self.shields = [Shield()]


    def execute (self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()   
        pygame.quit()            

    def run(self):
        # Game loop: events - update - draw
        pygame.mixer.music.play(-1)
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_ups_manager.reset_power_ups()
        self.player.has_power_up = False
        self.player.type = DEFAULT_TYPE
        self.score.score= 0
        self.death_count += 1

        while self.playing:
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
        
    
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        #self.obstacle_manager.update(self)
        self.obstacle_manager.update(self)
        self.score.update(self)
        self.power_ups_manager.update(self.game_speed, self.player, self.score)

    
    def draw(self):
        self.clock.tick(FPS)
        if self.score.score <= 1000:
            self.screen.fill((255, 250, 250)) 
        else:
            self.screen.fill((255, 87, 51)) #CAMBIA EL COLOR DEL FONDO SEGÚN EL PUNTAJE
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self)
        self.score.draw(self.screen)
        self.power_ups_manager.draw(self.screen)
        self.draw_power_up_active()        

        pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self): 
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        font_score = pygame.font.Font(FONT_STYLE, 30)
        font_menu_reatry = pygame.font.Font(FONT_STYLE, 60)
        font_dead_count = pygame.font.Font(FONT_STYLE, 100)

        if self.death_count == 0:
            font = pygame.font.Font(FONT_STYLE, 30)
            text_component = font.render("Press any key to play", True, (0,0,0) )
            text_rect = text_component.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text_component, text_rect)
            self.screen.blit(RUNNING[0], (half_screen_width -30, half_screen_height -140))

        if self.death_count > 0:
            self.game_speed = 20
            self.screen.fill((110, 0, 0))
            half_screen_height = SCREEN_HEIGHT // 2
            half_screen_width = SCREEN_WIDTH // 2
            ##########################################
            score_text = font_score.render(f"Points: {self.score.score} ", True, (0,0,0) )
            score_rect = score_text.get_rect()
            score_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(score_text, (score_rect.x +130, score_rect.y -250) )
            ##########################################
            score_text = font_score.render(f"Max Sore: {self.score.max_score}  | ", True, (0,0,0) )
            score_rect = score_text.get_rect()
            score_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(score_text, (score_rect.x -80, score_rect.y -250) )               

            ##########################################
            text_reatry = font_menu_reatry.render("Press any key to reatry", True, (255, 255, 255) )
            text_rect = text_reatry.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 230)
            self.screen.blit(text_reatry, text_rect)
            ############################################################
            dino_rotate = pygame.transform.scale(RUNNING[0], [220, 220])
            self.screen.blit(pygame.transform.rotate(dino_rotate, 180), (half_screen_width -100, half_screen_height -200))
            text_component = font_dead_count.render(f"deaths: {self.death_count}", True, (200, 100, 20) )
            text_rect = text_component.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 140)
            self.screen.blit(text_component, text_rect)

        pygame.display.update()
        self.handle_key_event_on_menu()

    def handle_key_event_on_menu (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death(self):
        self.playing = False
        self.death_count+=1

    def draw_power_up_active(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks())/1000)
            if time_to_show >=0:
                font = pygame.font.Font(FONT_STYLE, 30)
                powerup_text = font.render(f"Time left: {time_to_show} ", True, (0,0,0) )
                self.screen.blit(powerup_text, (1,1))
                pygame.display.update()
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE