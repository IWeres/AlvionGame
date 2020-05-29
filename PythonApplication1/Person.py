import pygame
import os
from Constants import *
from Projective import *
class Person():
    def __init__(self,game,name):
        self.game = game
        self.state = ALIVE
        self.direction = UP
        self.x = START_X
        self.y = START_Y
        self.lvl = 0
        self.exp = 0
        self.need_exp_to_next_lvl = 500
        self.name = name
        self.hp = MAX_HP
        self.mooving = [0,0,0,0]
        self.image_pack = ["data/personr1.png","data/persond1.png","data/personl1.png","data/personu1.png"]
        self.images = []
        self.spell_casted = 0
        self.load_states()
        for image in self.image_pack:
            temp = pygame.image.load(image).convert_alpha()
            i = []
            i.append(temp.subsurface(0,0,50,50))
            i.append(temp.subsurface(55,0,70,50))
            i.append(temp.subsurface(130,0,190,59))
            self.images.append(i)
            
    def is_file_exist(self):
        if os.path.isfile('./db.dll') != True:
            open("./db.dll","w+")
    
    def load_states(self):
        self.is_file_exist()        
        self.database = open("./db.dll","r")
        data = self.database.readlines()
        for x in data:
            data_array = x.split(";")
            self.lvl = int(data_array[0])
            self.exp = int(data_array[1])
        self.database.close()       
            
    def save_states(self):
        self.is_file_exist()
        self.database = open("./db.dll","w+")
        self.database.write(str(self.lvl) + ";" + str(self.exp))
        self.database.close()

    def moove(self):        
        if self.mooving[RIGHT] == 1:
            self.direction = RIGHT
            self.x += PLAYER_SPEED
        if self.mooving[DOWN] == 1:
            self.direction = DOWN
            self.y += PLAYER_SPEED
        if self.mooving[LEFT] == 1:
            self.direction = LEFT
            self.x -= PLAYER_SPEED
        if self.mooving[UP] == 1:
            self.direction = UP
            self.y -= PLAYER_SPEED

        if self.x <= 20: self.x = 20#20
        if self.y <= 30: self.y = 30#30
        if self.x >= SCREEN_WIDTH - 70: self.x = SCREEN_WIDTH - 70#80
        if self.y >= SCREEN_HEIGHT - 80: self.y = SCREEN_HEIGHT - 80 #90
        
        if self.x >= 24 and self.y >= 100 and self.x <= 100 and self.y <= 190:
            self.stop()
        if self.x >= 331 and self.y >= 430 and self.x <= 410 and self.y <= 505:
            self.stop()
        if self.x >= 600 and self.y >= 47 and self.x <= 706 and self.y <= 155:
            self.stop()
        if self.x >= 318 and self.y >= 187 and self.x <= 415 and self.y <= 305:
            self.bleed()




    def render(self,screen):
        screen.blit(self.images[self.direction][self.state],(self.x,self.y))

    def stop(self):
        if self.mooving[RIGHT] == 1:
            self.direction = RIGHT
            self.x -= PLAYER_SPEED
        if self.mooving[DOWN] == 1:
            self.direction = DOWN
            self.y -= PLAYER_SPEED
        if self.mooving[LEFT] == 1:
            self.direction = LEFT
            self.x += PLAYER_SPEED
        if self.mooving[UP] == 1:
            self.direction = UP
            self.y += PLAYER_SPEED
            
    def bleed(self):
        if self.mooving[RIGHT] == 1:
            self.direction = RIGHT
            self.x -= PLAYER_SPEED / 1.1
        if self.mooving[DOWN] == 1:
            self.direction = DOWN
            self.y -= PLAYER_SPEED / 1.1
        if self.mooving[LEFT] == 1:
            self.direction = LEFT
            self.x += PLAYER_SPEED / 1.1
        if self.mooving[UP] == 1:
            self.direction = UP
            self.y += PLAYER_SPEED / 1.1


    def render_ui(self,screen):
        screen.blit(pygame.image.load("data/hp.png"),(self.x + 8,self.y + 58))
        m = 1
        z = self.hp // 5
        while m <= z:
            screen.blit(pygame.image.load("data/hptick.png"),(self.x + 7 + m * 2,self.y + 59))
            m+=1

    def die(self):
        self.hp = 0
        self.state = DEAD   
        self.save_states()

    def tick(self):
        if self.state != DEAD:
            self.hp+=HP_REG
            if self.hp > MAX_HP:
                self.hp = MAX_HP
            if pygame.time.get_ticks() > self.spell_casted + 1000:
                self.state = ALIVE
            if self.hp <= 0:
                self.die()

    def add_exp(self, value):
        self.exp += int(value)
        if self.exp >= self.need_exp_to_next_lvl:
            self.lvl += 1
            self.exp = 0

    def shoot_e(self):
        if self.hp >= SKILL1_COST and self.state != SHOOT:
            self.hp-=SKILL1_COST
            self.state = SHOOT
            self.spell_casted = pygame.time.get_ticks()
            if self.direction == RIGHT:
                self.__shoot__(12,0)
            elif self.direction == DOWN:
                self.__shoot__(0,12)
            elif self.direction == LEFT:
                self.__shoot__(-12,0)
            else:
                self.__shoot__(0,-12)
    def __shoot__(self,x,y):
        self.game.projective.append(Fireball(self.game,self.x + x,self.y + y,self.direction))

    def __str__(self):
        return(self.name,self.x,self.y)
