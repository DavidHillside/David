
import sys

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''
    
    def __init__(self):
        pygame.init()
        
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion Game")
           
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
    

    def _create_alien(self, alien_number, row_number):
        '''create an alien and place it in a'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width +2*alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
       
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        
        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height)- ship_height)
        number_rows = available_space_y // (2*alien_height)
        
        #Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #create an alien and place it in the row.
                self._create_alien(alien_number, row_number)
    
    def _update_bullets(self):
        '''update position of bullets and get rid of old bullets.'''
         #update bullet positions
        self.bullets.update()
    
        
        # deletes bullets that go off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
#             print(len(self.bullets))
        
        collisions =  pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        
    def _check_keydown_events(self, event):
        '''respond to key presses'''
        if event.key == pygame.K_RIGHT:
            #move ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        '''respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        '''create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _check_events(self):
        #watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
               self._check_keyup_events(event)
    
    def _update_aliens(self):
        '''check if the fleet is at and edge then
            update the positions of all the aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()
        
    def _check_fleet_edges(self):
        '''respond appropriately if an alien reaches the edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        '''drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()