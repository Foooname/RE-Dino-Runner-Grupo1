import pygame
import random 
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.birds import Birds
from dino_runner.utils.constants import SMALL_CACTUS, BIRD
from dino_runner.components.powerups import powerup
from dino_runner.utils.constants import HAMMER, HAMMER_TYPE
from dino_runner.utils.constants import SHIELD, SHIELD_TYPE


class ObstacleManager:
    def __init__ (self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 1) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif random.randint(0, 1) == 0:
                self.obstacles.append(Birds(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
           
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE and game.player.type != HAMMER_TYPE: 
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.type == HAMMER_TYPE:
                    self.hammer_obstacle(game)
                else:
                    self.obstacles.remove(obstacle)
            
            elif game.player.dino_rect.colliderect(obstacle.rect):
                self.tries -= 1
                game.lives_manager.reduce_heart()
                if self.tries != 0:
                    self.obstacles.remove()
                    game.playing = True
                else:
                    pygame.time.delay(500)
                    game.death_count += 1
                    break

    def hammer_obstacle(self, game):
        for obstacle in self.obstacles:
            if game.player.dino_rect.colliderect(obstacle.rect):
                obstacle.rect.x += game.game_speed * 2
                obstacle.rect.y -= game.game_speed * 2
            if obstacle.rect.x > 1300:
                self.obstacles.pop()


    def draw(self, game):
        for obstacle in self.obstacles:
            obstacle.draw(game.screen)


    def reset_obstacles(self):
        self.obstacles = []