import pygame

# Initialize the game engine
pygame.init()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of the screen
size = (1200, 700)
screen = pygame.display.set_mode(size)
font = pygame.font.Font("digital-7.mono.ttf", 74)
 
 
pygame.display.set_caption("Wiktor's ping pong")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# Initialize the rectangle's position + direction
rect_x = 600
rect_y = 350
rect_change_x = -2.5
rect_change_y = 2.5


# Initialize the player paddle position + direction
paletka_gracza_x = 0
paletka_gracza_y = 350

y_speed = 0

# Initialize the AI paddle position
paletka_AI_x = 1180
paletka_AI_y = 350


human_score = 0
AI_score = 0

#sound
bounce_sound=pygame.mixer.Sound('pickupCoin.wav')
#image
background_image = pygame.image.load("Screenshot 2024-10-14 at 12.33.35.png").convert()



# Loop as long as done == False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Moving player paddle
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                y_speed = 0


    # Clear the screen and set the screen background
    screen.blit(background_image, [0,0])
    
    # Render the score text
    score_text = font.render(str(human_score) + " : " + str(AI_score), True, WHITE)

    # Display the score in the middle of the top of the screen
    screen.blit(score_text, [530, 40])

    # Draw the ball (rectangle)
    pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 40, 40])

    # Draw the boundaries (top and bottom)
    pygame.draw.rect(screen, WHITE, [0, 0, 1200, 30])
    pygame.draw.rect(screen, WHITE, [0, 670, 1200, 30])

    # Draw the player's paddle
    pygame.draw.rect(screen, WHITE, [paletka_gracza_x, paletka_gracza_y, 20, 100])

    # Draw the AI paddle
    pygame.draw.rect(screen, WHITE, [paletka_AI_x, paletka_AI_y, 20, 100])
    
    # Move the ball
    rect_x += rect_change_x
    rect_y += rect_change_y

    # Move player paddle
    paletka_gracza_y += y_speed

    # AI movement
    if paletka_AI_y < rect_y:
        paletka_AI_y += 0.9
    elif paletka_AI_y > rect_y:
        paletka_AI_y -= 0.9

    # Boundaries for player paddle
    if paletka_gracza_y < 30:
        paletka_gracza_y = 30  # Stop at the top
    elif paletka_gracza_y > 600:
        paletka_gracza_y = 600  # Stop at the bottom

    # Check if the ball hits the player's paddle
    if rect_x <= paletka_gracza_x + 20 and rect_x >= paletka_gracza_x and rect_y + 40 >= paletka_gracza_y and rect_y <= paletka_gracza_y + 100 and rect_change_x < 0:
        rect_change_x *= -1 
        bounce_sound.play()

    # Check if the ball hits the AI paddle
    if rect_x + 40 >= paletka_AI_x and rect_x + 40 <= paletka_AI_x + 20 and rect_y + 40 >= paletka_AI_y and rect_y <= paletka_AI_y + 100 and rect_change_x > 0:
        rect_change_x *= -1
        bounce_sound.play()

    # Reset the ball if it goes out of bounds (score condition)
    if rect_x < -50:  # AI scores
        rect_x, rect_y = 600, 350  # Reset ball position
        rect_change_x = 2.5  # Reset direction
        rect_change_y = 2.5
        AI_score += 1
        

    if rect_x > 1250:  # Human player scores
        rect_x, rect_y = 600, 350  # Reset ball position
        rect_change_x = -2.5  # Reset direction
        rect_change_y = -2.5
        human_score += 1

    # Bounce the ball off the top and bottom
    if rect_y > 629 or rect_y < 30:
        rect_change_y *= -1
        bounce_sound.play()

    # Update the screen
    pygame.display.flip()

    # Limit to 100 frames per second
    clock.tick(100)

# Be IDLE friendly
pygame.quit()
