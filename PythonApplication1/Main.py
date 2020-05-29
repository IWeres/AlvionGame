import pygame
from random import *
from Constants import *
from Person import *
from pygame.locals import *
from Projective import *
from Mob import *
from BigMob import *
from pygame import mixer
import sys


class Main():
    def __init__(self, screen):
        self.screen = screen        
        self.played_music = None
        self.person= Person(self,"Alvion")        
        self.bigmob = BigDemon(self,-500,-500,LEFT)
        self.projective= []
        self.mobs=[]
        self.mobs_to=[]
        self.background= pygame.image.load("data/background1test.png")
        self.background1=pygame.image.load("data/background.png")
        self.aboutimage=pygame.image.load("data/about.png")
        self.gameover_bg=pygame.image.load("data/gameover.png")
        self.gamewin_bg=pygame.image.load("data/gamewin.png")
        self.timer=pygame.time.Clock()
        self.running=True
        self.bigmob_created = False
        self.menu=True  
        self.__reinit()
        self.main_menu()        
       
    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:                    
                    return

    def muzika(self):
        if self.played_music is not None:
            self.played_music.stop()

        pygame.mixer.pre_init(44100,-16,1,512)
        pygame.mixer.init()
        sound=pygame.mixer.Sound('data/muzika1.wav')
        self.played_music = sound.play(-1)        
        return


    def gamewin(self):        
        screen.blit(self.gamewin_bg,(0,0))
        pygame.display.update()
        self.wait()

    def gameover(self):        
        screen.blit(self.gameover_bg,(0,0))
        pygame.display.update()
        self.wait()
        

    def about(self):
        screen.blit(self.aboutimage,(0,0))
        pygame.display.update()
        self.wait()
        

    def __reinit(self):
        self.muzika()
        self.person = Person(self,"Alvion")        
        self.bigmob = BigDemon(self,-500,-500,LEFT)
        self.projective= []
        self.mobs=[]
        self.mobs_to=[]        
        self.bigmob_created = False        
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type== QUIT: #реакцие на нажатие выхода
                self.running = False
            elif event.type==USEREVENT+1:
                self.person.tick()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.person.mooving=[1,0,0,0]
                if event.key == K_DOWN:                 #движение
                    self.person.mooving=[0,1,0,0]
                if event.key == K_LEFT:
                    self.person.mooving=[0,0,1,0]
                if event.key == K_UP:
                    self.person.mooving=[0,0,0,1]

                if event.key == K_e:
                    self.person.shoot_e()
                    

            elif event.type==KEYUP:
                if event.key==K_UP:
                    self.person.mooving[UP]=0     
                if event.key==K_DOWN:
                    self.person.mooving[DOWN]=0
                if event.key==K_RIGHT:                                       #при отжатии
                    self.person.mooving[RIGHT]=0
                if event.key==K_LEFT:
                    self.person.mooving[LEFT]=0


    def add_demon(self,x,y):
        self.mobs.append(Demon(self,x,y,LEFT))

    def add_big_demon(self,x,y):       
        self.bigmob.x = x
        self.bigmob.y = y
        self.mobs.append(self.bigmob)        

    
    def render(self):
        #self.screen.blit(self.background1,(0,0))#Прорисовка всего
        self.screen.blit(self.background,(0,0))
        self.person.render(screen)
        self.person.render_ui(screen)
        self.bigmob.render_ui(screen)
        for i in self.projective:
            i.render(screen)
        for i in self.mobs:
            i.render(screen)
        pygame.display.flip()
         # Text Renderer
    def text_format(self, message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
     
        return newText



    def close_game(self):
        try:
            self.menu = False
            self.running = False
            pygame.display.quit()            
            pygame.quit()
            exit()
        except:
            print("Выход из игры!")


    # Main Menu
    def main_menu(self):  
       selected="start"
       while self.menu:           
           for event in pygame.event.get():
               if event.type==pygame.QUIT:
                   self.close_game()
                   return
               if event.type==pygame.KEYDOWN:
                   if event.key==pygame.K_1:
                       selected="start"
                   if event.key==pygame.K_2:
                       selected="about"
                   if event.key==pygame.K_3:
                       selected="quit"
                       
                           
                   if event.key==pygame.K_RETURN:
                       if selected=="start":
                           self.main_loop()   
                       if selected=="quit":                                                      
                           self.close_game()
                       if selected =="about":
                           self.about()      
                           self.main_menu()
                           return

           if self.running != True:
               return
                           
    
           # Main Menu UI
           screen.blit(self.background1,(0,0))
           title=self.text_format("Alvion", font, 90, (255,215,0))
           exp=self.text_format("Опыта получено " + str(self.person.exp) + " из " + str(self.person.need_exp_to_next_lvl), font, 20,(255,255,224))
           lvl=self.text_format("ТЕКУЩИЙ УРОВЕНЬ " + str(self.person.lvl), font, 20,(255,255,224))
           if selected=="start":
               text_start=self.text_format("Начать", font, 75, WHITE)
           else:
               text_start = self.text_format("Начать", font, 75, BLACK)
           if selected=="quit":
               text_quit=self.text_format("Выход", font, 75, WHITE)
           else:
               text_quit = self.text_format("Выход", font, 75, BLACK)
           if selected =="about":
               text_about=self.text_format("О игре", font, 75, WHITE)
           else:
               text_about=self.text_format("О игре", font, 75, BLACK)
    
           title_rect=title.get_rect()
           start_rect=text_start.get_rect()
           quit_rect=text_quit.get_rect()
           about_rect=text_about.get_rect()
    
           # Main Menu Text
           screen.blit(title, (SCREEN_WIDTH/2 - (title_rect[2]/2), 120))
           if self.person.exp != 0:
                screen.blit(exp, (SCREEN_WIDTH/4 + 85 - (title_rect[2]/2), 80))
           screen.blit(lvl, (SCREEN_WIDTH/4 + 85 - (title_rect[2]/2), 60))
           screen.blit(text_start, (SCREEN_WIDTH/2 - (start_rect[2]/2), 300))
           screen.blit(text_about, (SCREEN_WIDTH/2 - (quit_rect[2]/2), 360))
           screen.blit(text_quit, (SCREEN_WIDTH/2 - (quit_rect[2]/2), 420))
           pygame.display.update()
           self.timer.tick(60)
           pygame.display.set_caption("Alvion")    
          

    

    def main_loop(self):        
        pygame.time.set_timer(USEREVENT+1,100)  
        counter = 100
        mobs_to_die = []
        mob_kills = 0
        while self.running==True:
           if len(self.mobs)<7:
               to = randint(0,3)
               self.mobs_to.append(to)
               x = randint(50,700)
               y = randint(50,500)
               isNotGood = True
               while(isNotGood):                   
                   isNotGood = False
                   x = randint(50,700)
                   y = randint(50,500)
                   if x >= 24 and y >= 100 and x <= 100 and y <= 190:
                       isNotGood = True
                   if x >= 331 and y >= 430 and x <= 410 and y <= 505:
                       isNotGood = True
                   if x >= 600 and y >= 47 and x <= 706 and y <= 155:
                       isNotGood = True

               self.add_demon(x,y)
                     
           if counter == 0:
               self.mobs_to = []
               counter = 100
               if mob_kills > 10 and self.bigmob_created != True:
                   self.add_big_demon(randint(50,700),randint(50,500))
                   self.bigmob_created = True
                   to = randint(0,3)
                   self.mobs_to.append(to)
                   mob_kills = 0

               for i in range(len(self.mobs)):
                   to = randint(0,3)
                   self.mobs_to.append(to)
                   if self.mobs[i-1].state == DEAD:
                       mobs_to_die.append(self.mobs[i-1])
                       mob_kills += 1

           if len(mobs_to_die) > 0 and counter == 25:       
               for i in mobs_to_die:
                   self.mobs.remove(i)
               mobs_to_die = []
           for i in range(len(self.mobs)):               
               speed = randint(1,7)
               self.mobs[i].moove(self.mobs_to[i],speed)
               if((self.mobs[i].x + 50 > self.person.x and self.mobs[i].x - 50 < self.person.x) and (self.mobs[i].y + 50 > self.person.y and self.mobs[i].y - 50 < self.person.y) and self.mobs[i].state != DEAD):
                   self.person.hp -= 2                 

           self.timer.tick(60)#основной цикл
           if self.person.state!=DEAD:
              self.person.moove()   
              #self.muzika()
           if self.person.hp < 1:
               self.person.die()               
               self.played_music.stop()
               pygame.mixer.pre_init(44100,-16,1,512)
               pygame.mixer.init()
               sound=pygame.mixer.Sound('data/ori2.wav')
               self.played_music = sound.play(-1)
               self.gameover()
               if self.running:
                   self.__reinit()
                   self.main_menu()
                
               
           if self.bigmob.hp < 1:
               self.bigmob.die()
               self.person.save_states()               
               self.played_music.stop()
               pygame.mixer.pre_init(44100,-16,1,512)
               pygame.mixer.init()
               sound=pygame.mixer.Sound('data/ori1.wav')
               self.played_music = sound.play(-1)
               self.person.add_exp(50)
               self.gamewin()
               if self.running:
                   self.__reinit()
                   self.main_menu()           
                

               

           for i in self.projective:
               if i.moove() != -1:                  
                   if((i.x + 30 > self.person.x and i.x - 30 < self.person.x) and (i.y + 30 > self.person.y and i.y - 30 < self.person.y)):   
                       self.person.hp -= 50
                       i.remove()                       

                   for j in self.mobs:
                       if((i.x + 30 > j.x and i.x - 30 < j.x) and (i.y + 30 > j.y and i.y - 30 < j.y) and j.state != DEAD):                       
                           i.remove()
                           if j.name != "BigDemon":
                               j.die()
                               self.person.add_exp(5)                               
                           else:
                               j.hp -= 50                                                                  
           
           if self.running:
               self.render()
           else: 
               return           

           self.handle_events()
           counter = counter - 1

    
            




pygame.init()
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game=Main(screen)
