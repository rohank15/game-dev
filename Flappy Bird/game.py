import pygame
import sys
from random import randint,choice

class Bird(pygame.sprite.Sprite):
    
    global game_active
    global pos_y
    pos_y = 300
    
    def __init__(self):
        super().__init__()
        
        self.steady = pygame.image.load('graphics/bird/bird_steady.png').convert_alpha()
        self.steady = pygame.transform.scale(self.steady,(60,60))
        
        self.fly = pygame.image.load('graphics/bird/bird_fly.png').convert_alpha()
        self.fly = pygame.transform.scale(self.fly,(60,60))
        
        self.index = 0
        self.frames = [self.steady,self.fly]
        
        self.pos_y = 300
        
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center = (400,300))
        self.rect = self.rect.inflate(-15,0)
        self.gravity = 0
        
    def key_pressed(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            self.gravity = -9
            self.index = 1
                      
    def jump(self):
        self.gravity += 1
        self.rect.y += self.gravity  
    
    def animation(self):
        self.image = self.frames[self.index]
        if self.index == 1:
            self.index = 0
    
    def reset(self):
        if self.rect.y > 600 or self.rect.y < 0:
            game_active = False
    
    def update(self):
        self.key_pressed()
        self.jump()
        self.animation()
        self.reset() 
               
class Pillar(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'Pillar':
            pillar_sprite = pygame.image.load('graphics/pillar/pillar.png').convert_alpha()
            pillar_sprite = pygame.transform.scale(pillar_sprite,(180,randint(100,300)))
            self.y_pos = 600
            
            self.image = pillar_sprite
            self.rect = self.image.get_rect(midbottom = (900,self.y_pos))
            self.rect = self.rect.inflate(0,-20)
        
        elif 'Pillar_Up':
            pillar_sprite = pygame.image.load('graphics/pillar/pillar_upsidedown.png').convert_alpha()
            pillar_sprite = pygame.transform.scale(pillar_sprite,(180,randint(100,300)))
            self.y_pos = -10 
            
            self.image = pillar_sprite
            self.rect = self.image.get_rect(midtop = (900,self.y_pos))
            self.rect = self.rect.inflate(0,-20)
           
    def destroy(self):
        if self.rect.x < -200:
            self.kill()
          
    def update(self):
        self.rect.x -= 5
        self.destroy()    

def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite,pillar,False):
        pillar.empty()
        return False
    else:
        
        return True

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
game_active = False
score = 0
x = 0                                                               

#Intro screen bird
bird_image = pygame.image.load('graphics/bird/bird_steady.png').convert_alpha()
bird_image = pygame.transform.scale(bird_image,(60,60))
bird_rect = bird_image.get_rect(center = (400,300))

#Backgroud
bg = pygame.image.load('graphics/background/bg.jpg')
bg = pygame.transform.scale(bg,(1102,600))
bg_rect = bg.get_rect(center = (400,300))

#Groups
bird = pygame.sprite.GroupSingle()
bird.add(Bird())
 
pillar = pygame.sprite.Group()

#Intro Screen
logo = pygame.image.load('graphics/logo/flappy-bird-logo-png-transparent.png').convert_alpha()
logo = pygame.transform.scale(logo,(600,160))
logo_rect = logo.get_rect(center = (400,150))

#Timer
pillar_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pillar_timer,randint(800,1000))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pillar_timer:
                pillar.add(Pillar(choice(['Pillar','Pillar_Up'])))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True     
        
    if game_active:
        screen.fill('black')
        
        screen.blit(bg,(x,0))
        x -= 1
        
        
        screen.blit(bg,(1102+x,0))
        
        if x == -1102:
            x = 0
        
        bird.draw(screen)
        bird.update()
        
        pillar.draw(screen)
        pillar.update()
        
        
        
        #collision
        game_active = collision_sprite()
    
    else:
        screen.fill('black')
        screen.blit(bg,(0,0))
        screen.blit(logo,logo_rect)
        screen.blit(bird_image,bird_rect)
        
        
    pygame.display.update()
    clock.tick(60)