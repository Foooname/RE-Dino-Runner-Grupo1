import pygame

from dino_runner.utils.constants import FONT_STYLE


class Score:
    def __init__(self):
        self.score = 0
        self.max_score = 0        
    def update(self, game):
        self.score +=1
        if self.score % 100 == 0:
            game.game_speed += 2
        if self.max_score < self.score:         # para obtener el maximo puntaje
            self.max_score = self.score
        


    def draw(self, screen):
        font = pygame.font.Font(FONT_STYLE, 22)
        text_component = font.render(f"Points: {self.score}", True, (0,0,0) )
        text_rect = text_component.get_rect()
        text_rect.center = (1000 ,50)
        screen.blit(text_component, text_rect)  

        font = pygame.font.Font(FONT_STYLE, 22)
        max_score_text = font.render(f"Max Score: {self.max_score}   |   ", True, (0,0,0) )
        text_rect = max_score_text.get_rect()
        text_rect.center = (850 ,50)
        screen.blit(max_score_text, text_rect)  

