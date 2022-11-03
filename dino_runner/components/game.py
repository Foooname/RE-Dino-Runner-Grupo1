import pygame

from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacles.obstacles_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SMALL_CACTUS, TITLE, FPS,RUNNING, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 200
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.death_count = 0
        self.score = Score()


    def execute (self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()   
        pygame.quit()            

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
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
        self.obstacle_manager.update(self)
        self.score.update(self)
        

    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self)
        self.score.draw(self.screen)

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
            self.screen.fill((110, 0, 0))
            half_screen_height = SCREEN_HEIGHT // 2
            half_screen_width = SCREEN_WIDTH // 2
            text_reatry = font_menu_reatry.render("Press any key to reatry", True, (255, 255, 255) )
            text_rect = text_reatry.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 230)
            self.screen.blit(text_reatry, text_rect)
            m = pygame.transform.scale(RUNNING[0], [220, 220])
            self.screen.blit(pygame.transform.rotate(m, 180), (half_screen_width -100, half_screen_height -200))
            text_component = font_dead_count.render(f"deaths: {self.death_count}", True, (200, 100, 20) )
            text_rect = text_component.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 140)
            self.screen.blit(text_component, text_rect)



            
            # Mostrar mensaje de volver a jugar () Listo
            #Mostrar el numero muertes actuales Listo
            #Mostrar el puntaje
        

        pygame.display.update()
        self.handle_key_event_on_menu()

    def handle_key_event_on_menu (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()