import pygame
from Constants import *
from Projective import *
class Mob():
    def __init__(self,game,name,x_start,y_start,image_pack):
        self.game=game
        self.state = ALIVE
        self.direction= UP
        self.x=x_start
        self.y=y_start
        self.name= name
        self.hp=MAX_HP
        self.mooving=[0,0,0,0]
        self.image_pack = image_pack
        self.images=[]
        self.spell_casted = 0
        for image in self.image_pack:
            temp=pygame.image.load(image).convert_alpha()
            i=[]
            i.append(temp.subsurface(0,0,50,50))
            i.append(temp.subsurface(55,0,70,50))
            i.append(temp.subsurface(100,0,190,59))#190
            self.images.append(i)


    def render(self,screen):
        screen.blit(self.images[self.direction][self.state],(self.x,self.y))

    
    def moove(self, to, speed):
        if self.state == DEAD: 
            return

        if to == 0:
            self.direction = RIGHT
            self.x += speed
        if to == 1:
            self.direction = DOWN
            self.y += speed
        if to == 2:
            self.direction = LEFT
            self.x -= speed
        if to == 3:
            self.direction = UP
            self.y -= speed 

        if self.x <=20: self.x=20
        if self.y <=30: self.y=30
        if self.x>= SCREEN_WIDTH - 80: self.x= SCREEN_WIDTH-80
        if self.y>= SCREEN_HEIGHT - 90: self.y= SCREEN_HEIGHT-90      

        if self.x >= 24 and self.y >= 100 and self.x <= 100 and self.y <= 190:
            self.stop(speed)
        if self.x >= 331 and self.y >= 430 and self.x <= 410 and self.y <= 505:
            self.stop(speed)
        if self.x >= 600 and self.y >= 47 and self.x <= 706 and self.y <= 155:
            self.stop(speed)
        if self.x >= 318 and self.y >= 187 and self.x <= 415 and self.y <= 305:
            self.bleed(speed)

    def die(self):     
        self.state=DEAD

    def stop(self, speed):            
        if self.direction == RIGHT:
            self.x -= speed
        if self.direction == DOWN:
            self.y -= speed
        if self.direction == LEFT:
            self.x += speed
        if self.direction == UP:
            self.y += speed
            
    def bleed(self, speed):
        if self.direction == RIGHT:
            self.x -= speed / 1.1
        if self.direction == DOWN:
            self.y -= speed / 1.1
        if self.direction == LEFT:
            self.x += speed / 1.1
        if self.direction == UP:
            self.y += speed / 1.1

class Demon(Mob):
    def __init__(self,game,x_start,y_start,dir):
        self.image_pack= ["data/mobr.png","data/mobd.png","data/mobl.png","data/mobu.png"]
        self.speed=30
        Mob.__init__(self,game,"Demon",x_start,y_start,self.image_pack)
            