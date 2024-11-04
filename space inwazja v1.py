import pygame
import random

from pygame.sprite import Group
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize font for displaying the score
pygame.font.init()
font = pygame.font.Font(None, 36)  # None for default font, 36 for font size

def display_score(screen, score):
    score_text = font.render(f"Score: {score}", True, WHITE)  # Render the score
    screen.blit(score_text, (10, 10))  # Display score at top-left corner

def display_health(screen, health):
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(health_text, (10, 40))

# Screen dimensions
SCREEN_WIDTH = 510
SCREEN_HEIGHT = 550

# Alien movement speeds and direction
alien_speed_x = 1  # Horizontal speed for aliens
alien_speed_y = 20  # Vertical movement when reaching edge
direction = 1  # 1 means right, -1 means left

# Aliens class 
class Aliens(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien.jpg").convert()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += alien_speed_x * direction  # Move horizontally

# Player class (different image)
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("soldier_space.png").convert()  # Load player image
        self.image.set_colorkey(GREEN)  # Set transparency if needed (assuming white background)
        self.rect = self.image.get_rect()

# Bullet class
class Bullet(pygame.sprite.Sprite): 
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png").convert()  # Set transparency if needed (assuming white background)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5  # Move bullet upward
        if self.rect.y < -10:  # If the bullet moves off the screen, kill it
            self.kill()

# Bomb class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bombimg.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5
        if self.rect.y > 600:
            self.kill()

# Helper function to check if an alien can drop a bomb
def can_drop_bomb(alien, aliens_list):
    """Check if an alien can drop a bomb (i.e., no alien is in front below it)."""
    for other_alien in aliens_list:
        if (other_alien.rect.x == alien.rect.x) and (other_alien.rect.y > alien.rect.y):
            return False  # Another alien is in front, so it cannot drop a bomb
    return True  # No alien in front, this alien can drop a bomb

""" Main Program """
pygame.init()

# Set the height and width of the screen (must happen before creating sprites)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Wiktor's Space Invasion")

back_image = pygame.image.load("gbackground.jpg").convert()

# Lists for sprites (initialize these first)
aliens_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()  # Create a group for bullets
bomb_list = pygame.sprite.Group()
 
# Player initialization (after defining the class)
player = Player()  # Now we can create a player object
all_sprites_list.add(player)

# Initialize health
health = 3

# Initialize score
score = 0

# Create aliens
pom_y = 20
pom_x = 20
sum = 1

# Set fixed spacing between aliens
alien_spacing_x = 50  # Horizontal spacing between aliens
alien_spacing_y = 50  # Vertical spacing between rows of aliens

for i in range(50):  # Create 50 aliens
    alien = Aliens()

    # Set the location for each alien
    alien.rect.x = pom_x
    alien.rect.y = pom_y

    aliens_list.add(alien)
    all_sprites_list.add(alien)

    # Move to the next column (fixed spacing)
    pom_x += alien_spacing_x

    # After 10 aliens, move to the next row
    if sum % 10 == 0:
        pom_y += alien_spacing_y  # Move down for the next row
        pom_x = 20  # Reset X position for the next row

    sum += 1  # Increment sum to keep track of the number of aliens

player_speed_x = 0

# Timer to control random bomb dropping
bomb_timer = 100  # Drop bombs more frequently
bomb_interval = random.randint(50, 100)  # Reduced interval for faster bomb drops

# Initialize the done flag to False
done = False  # This will control whether the game loop runs or stops
clock = pygame.time.Clock()  # This initializes the clock object

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed_x = -3
            elif event.key == pygame.K_RIGHT:
                player_speed_x = 3
            elif event.key == pygame.K_SPACE:  # Shoot bullet on spacebar press
                bullet = Bullet(player.rect.x + 20, player.rect.y)  # Create a bullet at the player's position
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)  # Add bullet to bullet group
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_speed_x = 0

    # Clear the screen before drawing
    screen.blit(back_image, (0, 0))  # Draw the background

    # Update player position
    player.rect.y = 500  # Fix player y-position
    player.rect.x += player_speed_x

    # Update all sprites (including player and bullets)
    all_sprites_list.update()

    # Check if any alien has reached the edge of the screen
    for alien in aliens_list:
        if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
            direction *= -1  # Reverse direction when hitting the edge
            for alien in aliens_list:
                alien.rect.y += alien_speed_y  # Move down all aliens by one row
            break  # Stop checking for edges once we reverse direction

    # Randomly drop bombs only from front-row aliens
    bomb_timer -= 1  # Decrease the bomb timer
    if bomb_timer <= 0:
        if len(aliens_list) > 0:  # Ensure there are aliens left
            front_row_aliens = [alien for alien in aliens_list if can_drop_bomb(alien, aliens_list)]  # Find aliens that can drop bombs
            
            if front_row_aliens:  # If there are any eligible aliens
                random_alien = random.choice(front_row_aliens)  # Select one random alien to drop a bomb
                bomb = Bomb(random_alien.rect.x, random_alien.rect.y)  # Drop a bomb from the selected alien
                all_sprites_list.add(bomb)
                bomb_list.add(bomb)
        
        # Reset the bomb timer with a new random interval
        bomb_timer = bomb_interval
        bomb_interval = random.randint(50, 100)  # Reset bomb interval

    # Handle collisions between bullets and aliens
    for bullet in bullet_list:
        alien_hit_list = pygame.sprite.spritecollide(bullet, aliens_list, True)
        
        if alien_hit_list:  # If the bullet hits any aliens
            bullet.kill()  # Kill the bullet
            for alien in alien_hit_list:  # Iterate through all hit aliens
                score += 1  # Increase the score for each alien hit
                print(score)

    player_group = pygame.sprite.GroupSingle(player)

    # Check if any alien has reached the player's position (the earth)
    for alien in aliens_list:
        if alien.rect.y >= player.rect.y - 20:  # Compare alien's y-coordinate with the player's y-coordinate
            done = True

    # Check for bomb collisions with player
    for bomb in bomb_list:
        player_hit_list = pygame.sprite.spritecollide(bomb, [player], False)

        if player_hit_list:
            bomb.kill()
            health -= 1  # Reduce health by 1 when hit by a bomb

            # End game when health reaches 0
            if health <= 0:
                done = True

    # Draw all the sprites
    all_sprites_list.draw(screen)

    # Control the frame rate
    clock.tick(60)
    
    display_score(screen, score)
    display_health(screen, health)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
