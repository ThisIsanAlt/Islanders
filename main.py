# Islander by Team Maple
# Made for Pyweek 30
# Code by MapleMaelstrom & ThisIsAnAlt
# Images by Amatol, Toastz and LegendaryChibi
# BGM by Amatol
# 2020-09-20 -> 2020-09-26

# Random allows for RNG, used all throughout this
import random
import sys
#time for limiting user inputs
import time
# Path, to allow images
from os import path
# Pygame, the source for it all
import pygame

FPS = 60
 
 # Adding directories
sprites_dir = path.join(path.dirname(__file__), 'sprites')
sounds_dir = path.join(path.dirname(__file__), 'sounds')
players_dir = path.join(path.dirname(__file__), 'players')
map_dir = path.join(path.dirname(__file__), 'map')

# ========================================== COLOUR DEFINITIONS =======================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
# ========================================== END OF - COLOUR DEFINITIONS ==============================================
 
# ======================================== INITIALIZE PYGAME AND CREATE WINDOW ========================================

##================================ VARIABLES ================================##
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
pygame.display.set_caption("Islanders")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("Calibri")
z, x, WIDTH, HEIGHT = screen.get_rect()
game_end = False
warning = False
 
# Sprite groups for collisions
 
all_sprites = pygame.sprite.Group()
interactables = pygame.sprite.Group()
chunks = pygame.sprite.Group()

try:
    # Loading and playing music - music made by Amatol
    
    pygame.mixer.music.load(path.join(sounds_dir, "Main_Theme.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    # Defining all sprites - player made by Toastz - 
    
    player_img = pygame.image.load(path.join(players_dir, "timmy.png")).convert()
    player_raft_img = pygame.image.load(path.join(sprites_dir, "raft.png"))
    tree_img = pygame.image.load(path.join(sprites_dir, "palm_tree.png"))
    log_img = pygame.image.load(path.join(sprites_dir, "log.png"))
    cave_tile = pygame.image.load(path.join(sprites_dir, "cave.png"))
    crafting_tile = pygame.image.load(path.join(sprites_dir, "table.png"))
    dock_img = pygame.image.load(path.join(sprites_dir, "dock.png"))
    berry_img = pygame.image.load(path.join(sprites_dir, "berry.png"))
    bg_img = pygame.image.load(path.join(map_dir, "background.png")).convert()
    map_img = pygame.image.load(path.join(map_dir, "island.png"))
    title_img = pygame.image.load(path.join(map_dir, "title.png"))
    keys_img = pygame.image.load(path.join(sprites_dir, "Arrow_Keys.png"))
except:
    print('WARNING: You do not have the correct dependencies installed. Please ensure that you have not made changes to the file structure, then try again.')
    warning = True
    
    

# Misc variables
speed = [0, 0]
lastMove = 0
defined = False
timeDiff = 0
game_start = False
done = False
doing_tutorial = False
tutorial_slide = 0
display_warning = False

##================================ FUNCTIONS ================================##

# For drawing text which is used quite a bit - maple
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    colour = color
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


# To draw the hunger bar - maple
def draw_hunger_bar(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(int(x), int(y), int(fill), int(BAR_HEIGHT))
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    draw_text(screen, "Hunger:", 15, int(x)-40, int(y)-2, BLACK)

##================================ CLASSES ================================##

# Player Class - Alt and Maple
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (20, 20))
        self.image.set_colorkey(WHITE)
        self.log_img = pygame.transform.scale(log_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
        self.speedx = 0
        self.speedy = 0
        self.hunger = 100
        self.wood = 0
        self.boat = 0
        self.isBoat = False
        self.last_regen = time.time()
        self.last_move = time.time()
        self.last_cave = time.time()
 
    def move(self, speed):
        if self.isBoat:
            self.rect.x += 3
            if self.rect.x >= WIDTH:
                return True
        elif self.hunger > 0 and (self.last_move + 0.1) < time.time() and ((WIDTH/2)+800 > self.rect.x + speed[0] > (WIDTH/2)-800 and ((HEIGHT/2)+500 > self.rect.y + speed[1] > (HEIGHT/2)-500)):
            self.rect.x += speed[0]
            self.rect.y += speed[1]
            if speed[0] != 0 or speed[1] != 0:
                self.hunger -= 1
            self.last_move = time.time()
        self.display()
        return False
 
    def display(self):
        screen.blit(self.image, [self.rect.x, self.rect.y])
        self.draw_logs()
    
    def add_hunger(self):
        if (self.last_regen + 1) < time.time() and self.hunger < 50:
            self.hunger += 1
            self.last_regen = time.time()
    
    def draw_logs(self):
        if self.boat == 0:
            screen.blit(self.log_img, (20, 20))
            if self.wood != 4:
                draw_text(screen, str(self.wood), 35, 80, 20, BLACK)
            else:
                draw_text(screen, str(self.wood), 35, 80, 20, GREEN)
        else:
            draw_text(screen, "YOU HAVE A BOAT!", 40, WIDTH/2, 20, BLACK)

    def become_boat(self):
        self.image = pygame.transform.scale(player_raft_img, (30, 30))
        self.isBoat = True

# Background class for bg images - Alt

class Background(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, width, height):        
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = round(x)
        self.rect.y = round(y)

    def update(self):
        screen.blit(self.image, [self.rect.x, self.rect.y])

# Interactable class for interactable objects - Maple

class Interactable(pygame.sprite.Sprite):
    def __init__(self, type, id, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == 'cave':
            self.image = pygame.transform.scale(cave_tile, (30, 30))
        elif self.type == 'tree':
            self.image = pygame.transform.scale(tree_img, (40, 40))
        elif self.type == 'table':
            self.image = pygame.transform.scale(crafting_tile, (20, 20))
        elif self.type == 'berry':
            self.image = pygame.transform.scale(berry_img, (20, 20))
        else:
            self.image = pygame.transform.scale(dock_img, (80, 60))
        self.rect = self.image.get_rect()
        self.id = id
        self.rect.x = x
        self.rect.y = y

    def interact(self):
        if self.type == 'cave':
            for i in interactables:
                if i.type == 'cave' and i.id != self.id:
                    time.sleep(3)
                    timmy.rect.x = i.rect.x
                    timmy.rect.y = i.rect.y
                    timmy.last_cave = time.time()
        elif self.type == 'tree':
            hits = pygame.sprite.spritecollide(timmy, interactables, True)
            timmy.wood += 1
        elif self.type == 'table' and timmy.wood == 4:
            timmy.boat = 1
            timmy.wood = 0
        elif self.type == 'dock' and timmy.boat == 1:
            timmy.become_boat()      
        elif self.type == 'berry':
            hits = pygame.sprite.spritecollide(timmy, interactables, True)
            timmy.hunger += 15

    def update(self):
        screen.blit(self.image, [self.rect.x, self.rect.y])
 
 # generating interactables
def generate():
    for i in range(18):
        while True:
            if WIDTH > 1650 and HEIGHT > 1050:
                randx = random.randrange((WIDTH / 2) - 700, (WIDTH / 2) + 700, 20)
                randy = random.randrange((HEIGHT / 2) - 400, (HEIGHT / 2) + 400, 20)
            else:
                randx = random.randrange((WIDTH / 2) - 400, (WIDTH / 2) + 400, 20)
                randy = random.randrange((HEIGHT / 2) - 300, (HEIGHT / 2) + 300, 20)
            break
        if i < 2:        
            newCave = Interactable('cave', i, randx, randy)
            interactables.add(newCave)
        elif 6 > i >= 2:
            newTree = Interactable('tree', i, randx, randy)
            interactables.add(newTree)
        elif i == 7:
            newTable = Interactable('table', i, randx, randy)
            interactables.add(newTable)
        elif 7 < i < 17:
            newBerry = Interactable('berry', i, randx, randy)
            interactables.add(newBerry)
        else:
            if WIDTH > 1650 and HEIGHT > 1500:
                newDock = Interactable('dock', i, WIDTH/2+700, HEIGHT/2)
            elif WIDTH > 1050 and HEIGHT > 850:
                newDock = Interactable('dock', i, WIDTH/2+475, HEIGHT/2)
            else:
                newDock = Interactable('dock', i, WIDTH/2+475, HEIGHT/2)
            interactables.add(newDock)

generate()
# Final declarations
if not warning:
    timmy = Player(player_img)
    background = Background(bg_img, 0, 0, WIDTH, HEIGHT)
    if WIDTH > 1650 and HEIGHT > 1500:
        island = Background(map_img, (WIDTH/2)-800, (HEIGHT/2)-500, 1600, 1000)
    else:
        island = Background(map_img, WIDTH/2-500, HEIGHT/2-400, 1000, 800)
    if WIDTH < 1050 or HEIGHT < 768:
        display_warning = True
    title_card = Background(title_img, WIDTH/2 - 200, HEIGHT/2 - 200, 400, 152)

# ======================================== END OF - INITIALIZE PYGAME AND CREATE ======================================
 
# ===================================================== GAME LOOP =====================================================
while not done:
    if game_start:
        timerStart = time.time() if not defined else timerStart
        defined = True
    # keep loop running at the right speed
    clock.tick(FPS)
    # --------------------------------------------------- UPDATE --------------------------------------------------
    if not warning and not display_warning:
        background.update()
        island.update()
        interactables.update()
    if game_start:
        if not timmy.isBoat:
            currentTime = time.time()
        timeDiff = round(currentTime - timerStart, 1)
        draw_text(screen, str(round(timeDiff, 1)), 30, WIDTH / 2, HEIGHT - 50, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                speed = [0, -20]
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                speed = [0, 20]
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                speed = [-20, 0]
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                speed = [20, 0]
            elif (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and (timmy.last_cave + 2) <= time.time():
                hits = pygame.sprite.spritecollide(timmy, interactables, False)
                for hit in hits:
                    hit.interact()
                    speed = [0, 0]
            elif event.key == pygame.K_SPACE:
                game_start = True if not display_warning else False
                display_warning = False
                print('display_warning is False')
            elif event.key == pygame.K_TAB:
                if not game_start:
                    if doing_tutorial:
                        tutorial_slide += 1
                    else:
                        doing_tutorial = True
            else:
                speed = [0, 0]
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                speed = [0, 0]
                lastMove = 0
    if not warning:
        game_end = timmy.move(speed)
        timmy.add_hunger()
        w, h = pygame.display.get_surface().get_size()
        draw_hunger_bar(screen, w - 320, 10, (timmy.hunger))

    # Menu Screen
    if not game_start and not doing_tutorial and not warning:
        fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (102, 112, 249), fill_rect)
        title_card.update()
        draw_text(screen, 'Press Space to begin', 30, WIDTH / 2, HEIGHT/2 - 20, BLACK)
        draw_text(screen, 'Press Tab for a tutorial', 30, WIDTH / 2, HEIGHT/2 + 30, BLACK)

    # Game End Screen
    if game_end:
        fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (102, 112, 249), fill_rect)
        draw_text(screen, 'You won!', 40, WIDTH / 2, HEIGHT/2 - 100, BLACK)
        draw_text(screen, f'Your time is: {timeDiff}', 30, WIDTH / 2, HEIGHT/2 - 20, BLACK)
        draw_text(screen, 'Press ESC to exit', 30, WIDTH / 2, HEIGHT/2 + 15, BLACK)
    # Tutorial Screen
    if doing_tutorial and not warning:
        if tutorial_slide == 0:
            fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(screen, (102, 112, 249), fill_rect)
            draw_text(screen, 'Use the arrow keys to move around the map.', 30, WIDTH/2, HEIGHT/2, BLACK)
            draw_text(screen, 'Press tab to continue.', 20, WIDTH/2, HEIGHT/2+135, BLACK)
            keys_image = pygame.transform.scale(keys_img, (100, 100))
            screen.blit(keys_image, ((WIDTH / 2) - 50, (HEIGHT / 2) - 100))
        elif tutorial_slide == 1:
            fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(screen, (102, 112, 249), fill_rect)
            draw_text(screen, 'Press Shift to interact with objects.', 30, WIDTH/2, HEIGHT/2, BLACK)
            draw_text(screen, 'Press tab to continue.', 20, WIDTH/2, HEIGHT/2+135, BLACK)
            cave_image = pygame.transform.scale(cave_tile, (100, 100))
            screen.blit(cave_image, ((WIDTH / 2) - 50, (HEIGHT / 2) - 100))
        elif tutorial_slide == 2:
            fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(screen, (102, 112, 249), fill_rect)
            draw_text(screen, 'Collect wood and craft it into a boat.', 30, WIDTH/2, HEIGHT/2, BLACK)
            draw_text(screen, 'Press tab to continue.', 20, WIDTH/2, HEIGHT/2+135, BLACK)
            wood_image = pygame.transform.scale(log_img, (100, 100))
            screen.blit(wood_image, ((WIDTH / 2) - 125, (HEIGHT / 2) - 100))
            craft_image = pygame.transform.scale(crafting_tile, (90, 90))
            screen.blit(craft_image, ((WIDTH / 2) + 25, (HEIGHT / 2) - 100))
        elif tutorial_slide == 3:
            fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(screen, (102, 112, 249), fill_rect)
            draw_text(screen, 'Use the dock to launch your boat and go back home!', 30, WIDTH/2, HEIGHT/2, BLACK)
            draw_text(screen, 'Press tab to finish.', 20, WIDTH/2, HEIGHT/2+135, BLACK)
            raft_image = pygame.transform.scale(player_raft_img, (100, 100))
            screen.blit(raft_image, ((WIDTH / 2) - 50, (HEIGHT / 2) - 100))
        elif tutorial_slide == 4:
            doing_tutorial = False

    # If an error has been made
    if warning:
        fill_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        draw_text(screen, 'You do not have the correct dependencies installed.', 40, WIDTH/2, HEIGHT/2, BLACK)
        draw_text(screen, 'Please ensure that you have not made changes to the file structure, then try again.', 40, WIDTH/2, HEIGHT/2+45, BLACK)
        draw_text(screen, 'Press ESC to exit.', 20, WIDTH/2, HEIGHT/2+150, BLACK)

    # If the screen resolution is too small
    if display_warning:
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        draw_text(screen, 'Your screen size is not supported.', 40, WIDTH/2, HEIGHT/2, BLACK)
        draw_text(screen, 'This game may not function properly if you proceed.', 40, WIDTH/2, HEIGHT/2+45, BLACK)
        draw_text(screen, 'Press ESC to exit, or SPACE to play.', 20, WIDTH/2, HEIGHT/2+150, BLACK)

    # --------------------------------------------------- DRAW ----------------------------------------------------
    # ---------------------------------------------- REFRESH THE SCREEN -------------------------------------------
    pygame.display.flip()
