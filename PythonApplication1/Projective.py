import pygame
from Constants import *

class Projective():
    def __init__(self,game,x_start,y_start,dir,image_pack):
        self.game=game
        self.x=x_start
        self.y=y_start
        if dir==RIGHT:            
            self.x+=5
        elif dir==DOWN:            
            self.y+=5
        elif dir==LEFT:            
            self.x-=5
        else:            
            self.y-=5
        self.direction=dir
        self.image=pygame.image.load(image_pack).convert_alpha()
        self.images=[]
        self.images.append(self.image.subsurface(0,0,60,60))
        self.images.append(self.image.subsurface(80,0,60,60))
        self.images.append(self.image.subsurface(150,0,60,60))
        self.images.append(self.image.subsurface(230,0,60,60))

    def render(self,screen):
        screen.blit(self.images[self.direction],(self.x,self.y))

    def moove(self):
        if self.x >= 34 and self.y >= 110 and self.x <= 110 and self.y <= 200:
            return self.remove()
        if self.x >= 341 and self.y >= 440 and self.x <= 420 and self.y <= 515:
            return self.remove()
        if self.x >= 610 and self.y >= 57 and self.x <= 716 and self.y <= 165:
            return self.remove()
        if self.x >= 318 and self.y >= 187 and self.x <= 415 and self.y <= 305:
            self.bleed(self.speed)
                    
        if self.direction==RIGHT:            
            self.x+=self.speed
        elif self.direction==DOWN:            
            self.y+=self.speed
        elif self.direction==LEFT:            
            self.x-=self.speed
        else:            
            self.y-=self.speed

        if self.x>SCREEN_WIDTH or self.x<-32 or self.y>SCREEN_HEIGHT or self.y<-32:
            return self.remove()

    def remove(self):        
        if self in self.game.projective:
            self.game.projective.remove(self)
        return -1

    def bleed(self,speed):
        if self.direction == RIGHT:
            self.x -= speed / 1.01
        if self.direction == DOWN:
            self.y -= speed / 1.01
        if self.direction == LEFT:
            self.x += speed / 1.01
        if self.direction == UP:
            self.y += speed / 1.01

    def __str__(self):
        return(self.x,self.y)
                                    
class Fireball(Projective):
    def __init__(self,game,x_start,y_start,dir):
        self.image= "data/fireball.png"
        self.speed=30
        Projective.__init__(self,game,x_start,y_start,dir,self.image)
        pygame.mixer.pre_init(44100,-16,1,512)
        pygame.mixer.init()
        sound=pygame.mixer.Sound('data/shoot.wav')
        sound.play()

