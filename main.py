# importing PyGame package
import pygame
from pygame import mixer
import time
import random
import os

# initialise PyGame package
mixer.init()
pygame.init()

# game-screen dimensions
SCREEN_WIDTH = 1280                                             # ~capitalisation added to show-
SCREEN_HEIGHT = 720                                             # -that the values are constant~

# game-window configuration settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # screen size
pygame.display.flip()                                           # refresh the game-window background
pygame.display.set_caption("One Bump")                          # display name on window

# game-window frame settings
clock = pygame.time.Clock()
FPS = 60                                                        # set the frame rate

# load music and sounds
theme = pygame.mixer.Sound('assets/theme.mp3')
theme.set_volume(0.1)
theme_playing = False
jump_sfx = pygame.mixer.Sound('assets/jump.mp3')
jump_sfx.set_volume(0.5)
death_sfx = pygame.mixer.Sound('assets/death.mp3')
death_sfx.set_volume(1)

# game properties
scroll_threshold = 250
scroll = 0
bg_scroll = 0
max_platforms = 10
game_over = False
fade_counter = 0
# game variables
GRAVITY = 1
score = 0
altitude = 0
movement_speed = 15
bounce_speed = 25
# peak altitude
if os.path.exists('altitude.txt'):
    try:
        with open('altitude.txt') as file2:
            top_altitude = int(file2.read())
    except ValueError:
        top_altitude = 0
else:
    top_altitude = 0
# peak high score
if os.path.exists('score.txt'):
    try:
        with open("score.txt", "r") as file:
            high_score = int(file.read())
    except ValueError:
        high_score = 0
else:
        high_score = 0

# define variables for colour and font
COLOUR = (255, 255, 255)
BLACK = (0,0,0)
font_small = pygame.font.SysFont('Bahnschrift',30)
font_med = pygame.font.SysFont('Bahnschrift',42)
font_big = pygame.font.SysFont('Bahnschrift',69)

# load the assets
img_background = pygame.image.load('assets/background.png').convert_alpha()
img_character = pygame.image.load('assets/dino.png').convert_alpha()
img_platforms = pygame.image.load('assets/clouds.png').convert_alpha()

# functions
def draw_bg(bg_scroll):
    screen.blit(img_background, (0, 0 + bg_scroll))
    screen.blit(img_background, (0, -720 + bg_scroll))

def draw_panel():
    pygame.draw.line(screen, BLACK, (0, 60), (SCREEN_WIDTH, 60), 3)
    draw_text('Score: ' + str(score), font_small, BLACK, 0, 0)
    draw_text(f'Altitude: {str(altitude)}m', font_small, BLACK, 0, 30)

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

# character classes
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(img_character, (90,90))
        self.width = 40                                         # ~adjust character's height and width-
        self.height = 72                                        # -ensure they are in 9(height):5(width) format~
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.flip = False
    # move the character
    def move(self):

        # reset variables
        scroll = 0
        dy = 0                                                  # change in y-coordinate
        dx = 0                                                  # change in x-coordinate

        # process the keys being pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx -= movement_speed                               # adjust left movement speed
            self.flip = False
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx += movement_speed                               # adjust right movement speed
            self.flip = True

        # gravity property
        self.vel_y += GRAVITY
        dy += self.vel_y

        # check colliion with side barriers
        if self.rect.left + dx < 280:                           # check for left side
            dx =280 - self.rect.left
        if self.rect.right + dx > 1000:                         # check for right side
            dx = 1000 - self.rect.right

        # check collision with platforms
        for platform in group_platforms:                        # check collision with each platform
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if platform above
                if self.rect.bottom < platform.rect.centery:
                    # if falling
                    if self.vel_y > 0:
                        # bounce character back up
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -bounce_speed              # bounce height off of
                        jump_sfx.play()


        # check if scroll_threshold reached
        if self.rect.top <= scroll_threshold:
            # if player if jumping
            if self.vel_y < 0:
                scroll = -dy                                    # scroll variable should be opposite of dy
                                                                # (negative since character is moving Up)

        # update rectangle's position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False),# displaying the image flipped if self.flip is True
            (self.rect.x - 20, self.rect.y))                    # position the rect (boundary) smaller than the actual image

# platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img_platforms, (width,height) )
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.rectheight = height + 10
        self.rect = pygame.Rect(0,0, width, self.rectheight)
        self.rect.x = x
        self.rect.y = y

    # when called will update the platform's position to match with character's scroll
    def update(self, scroll):
        # moving platforms
        if self.moving == True:
            self.move_counter += 1
            if altitude < 5000:
                directional_speed = 1
            elif altitude > 5000 and altitude < 10000:
                directional_speed = 2
            else:
                directional_speed = random.randint(2,5)
            self.rect.x += self.direction * directional_speed
        # change platform direction
        #
        if altitude < 5000:
            directional_movement = 100
        elif altitude > 5000 and altitude < 10000:
            directional_movement = 250
        else:
            directional_movement = 500
        # change direction
        if self.move_counter >= directional_movement or (self.rect.left < 280) or (self.rect.right > 1000):
            self.direction *= -1
            self.move_counter = 0

        # update platform's y-position
        self.rect.y += scroll

        # check if platform invisble
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            global score
            score += 1


# character instance
character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75)


# creating sprite groups
group_platforms = pygame.sprite.Group()

# creating starting platform
platform = Platform((SCREEN_WIDTH // 2) - 35 , SCREEN_HEIGHT - 40, 95.2, 40, False)
group_platforms.add(platform)


running = True                                                  # boolean value for the loop condition
# looping to keep game-window open until stopped
while running:

    clock.tick(FPS)

    # if game is running
    if game_over == False:
        # play theme if not already playing
        if theme_playing == False:
            theme.play()
            # theme is playing so var set to true
            theme_playing = True

        # scroll is set to character's movement
        scroll = character.move()
        bg_scroll += scroll
        if bg_scroll >= 720:
            bg_scroll = 0

        # display background
        draw_bg(bg_scroll)

        # creating platforms
        if len(group_platforms) < max_platforms:
            platform_height = int(random.randint(40, 60))     # randomised height of clouds
            platform_width = 2.38 * platform_height                 # multiplied by 2.38 to maintain aspect ratio
            # adjust distance of one platform from another
            platform_x = random.randint(280, 1000 - 60)
            # adjust height of one platform from another
            platform_y = platform.rect.y - random.randint(150,200)
            # biased probability platform_moving is True based on altitude
            platform_type = int(random.randint(1, 8))
            # if altitude is less than 5k, probability it is moving is 1/8 or ~13%
            if altitude < 5000:
                if platform_type == 1:
                    platform_moving = True
                else:
                    platform_moving = False
            # if altitude is more than 5k and less than 10k, probability it is moving is 3/8 or ~38%
            elif altitude > 5000 and altitude < 10000:
                if platform == 1 or 2 or 3:
                    platform_moving = True
                else:
                    platform_moving = False
            # if altitude is above 10k, probabiliy it is moving is 6/8 or 75%
            else:
                if platform == 1 or 2 or 3 or 4 or 5 or 6:
                    platform_moving = True
                else:
                    platform_moving = False
            # plug in the platform values
            platform = Platform(platform_x, platform_y, platform_width, platform_height, platform_moving)
            # add the platform to the platform group, which acts as a counter
            group_platforms.add(platform)

        # update platforms
        group_platforms.update(scroll)

        # update altitude
        if scroll > 0:
            altitude += scroll

        # draw high_score marker
        altitude_y = (altitude - top_altitude + scroll_threshold)
        pygame.draw.line(screen, BLACK, (0, altitude_y), (SCREEN_WIDTH, altitude_y), 2)
        draw_text('High Score line', font_small, BLACK, 0, altitude_y - 30 )
        if altitude < top_altitude:
            draw_text(f'High score in {top_altitude - altitude}m', font_small, BLACK, 990, 30)

        # display platforms
        group_platforms.draw(screen)
        # display character
        character.draw()
        # display score panel
        draw_panel()

        # check if game_over is True (if player fell off screen)
        if character.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_sfx.play()
    # if the game is over
    else:
        theme.stop()
        # display fading animation after death
        if fade_counter < (SCREEN_WIDTH // 2):
            fade_counter += 30
            pygame.draw.rect(screen, BLACK, (0, 0, fade_counter, SCREEN_HEIGHT))
            pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH - fade_counter), 0, fade_counter, SCREEN_HEIGHT))
        else:
            # draw game over text after animation
            draw_text('Game Over!', font_big, COLOUR, (SCREEN_WIDTH // 2) - 200, (SCREEN_HEIGHT // 2))
            draw_text('Score: ' + str(score), font_small, COLOUR, (SCREEN_WIDTH // 2) - 195, (SCREEN_HEIGHT // 2) - 42)
            draw_text('Press [SPACE] to continue', font_med, COLOUR, (SCREEN_WIDTH // 2) - 195, (SCREEN_HEIGHT // 2) + 69)
            # update high_score
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))
            if altitude > top_altitude:
                top_altitude = altitude
                with open("altitude.txt", "w") as file2:
                    file2.write(str(top_altitude))
            # if SPACE key pressed, restart game
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # reset variables
                theme_playing = False
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                altitude = 0
                # reposition the character
                character.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75)
                # reset platforms
                group_platforms.empty()
                platform = Platform((SCREEN_WIDTH // 2) - 35, SCREEN_HEIGHT - 40, 95.2, 40, False)
                group_platforms.add(platform)


    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # constant game-screen update
    pygame.display.update()
    pygame.display.flip()

pygame.quit()