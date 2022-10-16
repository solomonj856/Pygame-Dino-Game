import pygame 
import sys
import random

pygame.init() #initializes pygame


screen_width = 700
screen_height = 500
     
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))         
pygame.display.set_caption("Dino Jump") #game title

  

class Enemy(pygame.sprite.Sprite): #cactus enemy
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cactus.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (800, 400)
        self.speed = -10 #speed of enemy
        

    def update(self, group):
        
        ground = group.sprite
        self.rect.bottom = ground.rect.top #sets enemy on top of ground
        self.rect.x += self.speed
        if self.rect.left < -100:
            S1.score += 1
            self.rect.x =  800
        #if score reaches 10, make speed faster
        if S1.score == 10:
            self.speed = -15

class Enemy_2(pygame.sprite.Sprite): #bird enemy
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bird.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (900, 305)
        self.speed = -7
    
    def update(self, group):
        #ground = group.sprite
        self.rect.x += self.speed
        if self.rect.left < -200:
            S1.score += 1
            self.rect.x = random.choice((900, 1300, 1700)) #picks random starting positions
        
        if S1.score == 10:
            self.speed  = -12

            
    
class Player(pygame.sprite.Sprite): #dinosaur player
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dinosaur.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80,80))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()    
        self.rect.center = (150, 400)
        self.jump = -32
        self.gravity = 2
        self.direction = pygame.math.Vector2(0,0)
    

    def jumping(self): #jump function

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.direction.y = self.jump


        
    def update(self, group, enemies):
        #constant gravity
        self.direction.y += self.gravity
        
        self.rect.y += self.direction.y 
        #single sprite of ground
        ground = group.sprite 
    
        
        if pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask):
            self.direction.y = 0 #sets gravity to 0
            self.rect.bottom = ground.rect.top 
            self.jumping() #calls the ability to jump when on the ground
                
        
        if pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask): #if collide with enemy, quit game
             game_over()
          
    

class Ground(pygame.sprite.Sprite): #green ground
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ground.png").convert_alpha()              
        self.rect = self.image.get_rect()
        self.rect.center = (350, 480)


class Cloud(pygame.sprite.Sprite): #background clouds
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("cloud.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x + 200
        
    
    def move(self): #movement
        self.rect.x -= 1
        if self.rect.x < -200:
            self.rect.x = self.x

    

class Score(pygame.sprite.Sprite): #text score
    def __init__(self):
        super().__init__()
        self.white = (255,255,255)
        self.font = "Arial Bold"
        self.size = 60
        self.score = 0
        
    

    def update(self):
        #creates font
        self.my_font = pygame.font.SysFont(self.font, self.size)
        text_surface = self.my_font.render(f"Score: {self.score}", True, self.white)
        screen.blit(text_surface, (25,25))

        #adds bird enemy
        if self.score == 5:
            Enemygroup.add(E2)
            E2.update(Groundgroup)
        #updates bird      
        if self.score > 5:
            E2.update(Groundgroup)
        
        
def create_text(font, size, string, colour, pos):
    displayfont = pygame.font.SysFont(font, size)
    textsurface = displayfont.render(string, True, colour)
    screen.blit(textsurface, pos)

def game_over():
    while True:
        screen.fill((3,194,252))
        create_text("Arial Bold", 75, "Game Over", (255,50, 42), (200, 125))
        create_text("Arial Bold", 75, f"Final score: {S1.score}", (255,255,255), (180, 220))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

#class variables
P1 = Player()
E1 = Enemy()
G1 = Ground()
S1 = Score()
E2 = Enemy_2()

#different pos for clouds
C1 = Cloud(600, 100)
C2 = Cloud(700, 200)


#sprite groups

Playergroup = pygame.sprite.GroupSingle()
Playergroup.add(P1)

Enemygroup = pygame.sprite.Group()
Enemygroup.add(E1)

Groundgroup = pygame.sprite.GroupSingle()
Groundgroup.add(G1)

Cloudgroup = pygame.sprite.Group()
Cloudgroup.add(C1)
Cloudgroup.add(C2)


sun = pygame.image.load("sunny.png").convert_alpha()


while True: #game loop

    screen.fill((104, 149, 255)) #background image
    screen.blit(sun, (550, -90))

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 

    
    P1.update(Groundgroup, Enemygroup) #player
    E1.update(Groundgroup) #enemy
    C1.move() #cloud1
    C2.move() #cloud2
    
    
    #shows sprites on screen
    
    Enemygroup.draw(screen)
    Groundgroup.draw(screen)
    Cloudgroup.draw(screen)
    Playergroup.draw(screen)
        

    S1.update() #text




    pygame.display.update() #updates screen
    clock.tick(60) #60 fps



