

# Image by <a href="https://pixabay.com/users/dawnydawny-2157612/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2442125">dawnydawny</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2442125">Pixabay</a>

import pygame

class Ship:
    def __init__(self, ai_game):
        
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        self.settings = ai_game.settings
        
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
       
        self.rect.midbottom = self.screen_rect.midbottom
        
       
        self.x = float(self.rect.x)
        
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        
        self.rect.x = self.x
    
    def blitme(self):
        
        self.screen.blit(self.image, self.rect)