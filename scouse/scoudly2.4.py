#!/usr/bin/env python
# -*- coding: utf-8 -*
################################################################################
#                                                         #    PYTHON 3.1.2    #
#                                                         ######################
# Auteur du présent code : Deregnaucourt Maxime           #   WINDOWS TESTED   #
#                        : space.max@free.fr              ######################
#                                                         #  LINUX  NOT TESTED #
# Thank you to Pygame's team                              ######################
# Merci à Maya et Gabriel pour leur talent artistique                          #
################################################################################


import pygame, random, sys 
from pygame.locals import *

#Variables Globales
global rouge,vert,bleu,noir,jaune,orange,blanc,effect,x,max_level,fps,laps,laps_power 
rouge=(255,0,0) 
vert=(0,255,0) 
bleu=(0,0,255) 
noir=(0,0,0) 
jaune=(255,255,0) 
orange=(255,140,0) 
blanc=(255,255,255)
max_level=10
fps=50
laps=30000
laps_power=7000
pygame.init()
def clavier():

    pygame.event.get() 
    if pygame.key.get_pressed()[K_ESCAPE]:
        sys.exit()
    elif pygame.key.get_pressed()[K_LEFT]:
        #scoudly.bouge("left")
        ecran.allScoudly.update("left")
        if pygame.key.get_pressed()[K_SPACE] and ecran.power=="On":
            ecran.allScoudly.update("left","space")
            #scoudly.bouge("left","space")
        else: 
            ecran.allScoudly.update("left","")
            #scoudly.bouge("left","")
            scoudly.diminue()  
    elif pygame.key.get_pressed()[K_RIGHT]:
        #scoudly.bouge("right")
        ecran.allScoudly.update("right")
        if pygame.key.get_pressed()[K_SPACE] and ecran.power=="On":
            #scoudly.bouge("right","space")
            ecran.allScoudly.update("right","space")
        else: 
            ecran.allScoudly.update("right")
            #scoudly.bouge("right")
            scoudly.diminue()  
    elif pygame.key.get_pressed()[K_SPACE] and ecran.power=="On":
        scoudly.grandit()
    elif not pygame.key.get_pressed()[K_SPACE]:
        scoudly.diminue()

def music_fond():
    pygame.mixer.music.load("./sound/music03.ogg")
    pygame.mixer.music.play(-1,0)

def wait(laps):
    pygame.time.wait(laps)

class Scoudly(pygame.sprite.Sprite):
    
    def __init__(self,x=184,y=0,ind=0,nb_anneaux=5):
        #x=snake.fond[0][1].left-32,ind=2,nb_anneaux=nb_anneaux)
        pygame.sprite.Sprite.__init__(self) 
         
        #Les variables
        self.vie=3
        self.nb_anneaux=nb_anneaux
        self.ecart=0
        self.top=y
        self.left=x
        self.sens=0
        self.score=2*[0]
                
        # Le tableau des images  du serpent
        # Table of image,Rect of the snake 
        self.fond=[]
        
        # The head : Dimension (32x32)
        
        self.img0=pygame.image.load("./graph/scoudly01.png").convert_alpha()
        self.fond.append([self.img0,self.img0.get_rect()])
        self.fond[0][1].left=self.left
        #print(self.fond)
        # Les anneaux / The rings of the body: Dimension (32 x 15)
       
        self.img1=pygame.image.load("./graph/anneau01.png").convert_alpha()
        
        for i in range(self.nb_anneaux):
            # Couple Image,Rect
            self.fond.append([self.img1,self.img1.get_rect()])
              
        # La Queue / The Queue: Dimension (32 x 6)
        
        self.img2=pygame.image.load("./graph/queue.png").convert_alpha()
        self.fond.append([self.img2,self.img2.get_rect()])
        
        
        # Blit Snake at the middle of the screen
        self.affiche_tete()
        i=1
        while i<len(self.fond):
                  
          self.top=self.top-self.fond[i][1].height
          self.fond[i][1].top=self.top
          # Alignement sur la tête
          self.fond[i][1].left=self.fond[0][1].left
          ecran.surface.blit(self.fond[i][0],self.fond[i][1])
          i+=1
        
        self.image=pygame.Surface((0,0)).convert_alpha()
        self.rect=self.image.get_rect()
        
        self.ind=ind
        ecran.allScoudly.add(self)
        
    def affiche_tete(self):
        
        # Affiche la Tête
        var=20
        # Calcul de la position de la tête
        self.top=(len(self.fond)-2)*self.fond[1][1].height+self.fond[-1][1].height+var
        self.fond[0][1].top=self.top
        self.fond[0][1]=self.fond[0][1].move(self.sens,0)
        ecran.surface.blit(self.fond[0][0],self.fond[0][1])                  
    
    def affiche(self):
        
        self.affiche_tete()
        
        # Affiche les anneaux
        i=1
        while i<len(self.fond)-1:
            self.top=self.top-self.fond[i][1].height
            self.fond[i][1].top=self.top
            # Test appuie touche left et right
            cond=pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_RIGHT]
            if not cond:
                self.sens=0
            # Calcul ecart entre tête et anneaux
            self.ecart=(self.fond[0][1].left-self.fond[i][1].left)/6
            val=6
            if cond==1:
                if abs(self.ecart)>i:
                    if self.ecart<0:
                        self.fond[i][1].left=self.fond[i][1].left-val
                        self.ecart+=1
                    elif self.ecart>0: 
                        self.fond[i][1].left=self.fond[i][1].left+val
                        self.ecart-=1
            else:
                if self.ecart<0:
                      self.fond[i][1].left=self.fond[i][1].left-val
                      self.ecart+=1
                elif self.ecart>0: 
                      self.fond[i][1].left=self.fond[i][1].left+val
                      self.ecart-=1
            ecran.surface.blit(self.fond[i][0],self.fond[i][1])
            i+=1

        # Alignement Queue sur dernier anneau           
        self.fond[-1][1].left=self.fond[-2][1].left
        ecran.surface.blit(self.fond[-1][0],self.fond[-1][1])
    
    def update(self,sens,space=""): 
        
        # Calcul du minleft et du maxright
        
        # Un serpent
        if len(ecran.allScoudly)==1:
            self.minleft=0
            self.maxright=ecran.size[0]
        
        # Deux serpents
        elif len(ecran.allScoudly)==2:
            # Pour le serpent 1, la limite gauche vaut la limite droite du serpent 2
            if self.ind==1:
                for s in ecran.allScoudly:
                    if s.ind==2:
                        self.minleft=s.fond[0][1].right
                        self.maxright=ecran.size[0]
            # Pour le serpent 2, la limite droite vaut la limite gauche du serpent 1
            # La limite gauche vaut 0
            elif self.ind==2:
                self.minleft=0
                for s in ecran.allScoudly:
                    if s.ind==1:
                        self.maxright=s.fond[0][1].left
                # Trois serpents
        elif len(ecran.allScoudly) == 3:
            # Pour le serpent 1, la limite gauche vaut la limite droite du serpent 2
            # La limite droite vaut la limite gauche du serpent 3
            if self.ind == 1:
                for s in ecran.allScoudly:
                    if s.ind == 2:
                        self.minleft = s.fond[0][1].right
                    elif s.ind == 3:
                        self.maxright = s.fond[0][1].left

            # Pour le serpent 2, la limite droite vaut la limite gauche du serpent 1
            # La limite gauche vaut 0
            elif self.ind == 2:
                self.minleft = 0
                for s in ecran.allScoudly:
                    if s.ind == 1:
                        self.maxright = s.fond[0][1].left

            # Pour le serpent 3, la limite gauche vaut la limite droite du serpent 1
            # La limite droite vaut la limite de l'écran
            elif self.ind == 3:
                self.maxright = ecran.size[0]
                for s in ecran.allScoudly:
                    if s.ind == 1:
                        self.minleft = s.fond[0][1].right

        self.affiche()
        '''
        for i, s in enumerate(ecran.allScoudly):
            if i == 2:  # Le troisième élément a l'index 2 (car les indices commencent à 0)
                print(vars(s))
                break  # Sort de la boucle après l'affichage))
        '''    
        if sens=="left" and self.fond[0][1].left>self.minleft:
            self.sens=-6
        elif sens=="right" and self.fond[0][1].right<self.maxright:
            self.sens=6
        else:
            self.sens=0
        if space=="space":
            self.grandit()
                   
    def grandit(self):
        
        for s in ecran.allScoudly:
        # Récupère le rect du dernier anneau
        
            if len(s.fond)<40:
                lastRect=s.fond[-2][1]
                lastRect=lastRect.move(0,-15)
                s.fond.append([s.img1,lastRect])
                anneau=s.fond[-1]
                # Remet la queue en dernier
                s.fond[-1]=s.fond[-2]
                s.fond[-2]=anneau
       
    def diminue(self):
        
        for s in ecran.allScoudly:
            if len(s.fond)>s.nb_anneaux+2:
                del s.fond[1]           

class Ecran(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        self.highscore=[]
        self.game_timer=0
        self.power_timer=0
        self.tps=0
        self.vie=3
        self.score=0
        self.niveau=0
        self.power="Off"
        self.level_time=[]
        # The laps per level
        self.laps=laps
        #
        # numbers of levels
        #
        for o in range(max_level+1):
            self.level_time.append((o+1)*self.laps)
       
        # Width, Height
        self.size=(width,height)=(400,800)
        self.surface=pygame.display.set_mode(self.size)
        pygame.display.set_caption('Scoudly by space.max@free.fr')
        
        #Chargement des images
       
        self.bg=pygame.image.load("./graph/highscore.png").convert_alpha()
        self.bgRect=self.bg.get_rect()
   
        self.cursor=pygame.image.load("./graph/scoudly.left.png").convert_alpha()
        self.cursorRect=self.bg.get_rect()
        
        self.rule=pygame.image.load("./graph/rule.png").convert_alpha()
        self.ruleRect=self.rule.get_rect()
        
        # TO DO Add Scoudly Image here
        
        #-----------------------------------------------
        # Group for the Snakes
        #-----------------------------------------------
        self.allScoudly=pygame.sprite.RenderUpdates()
    
        
        self.surface.fill(noir)

        # la nourriture        
        self.food=[]
        
        self.son01=pygame.mixer.Sound("./sound/china.wav")
        
    def make_clock(self):
    
        # This clock is used for the timming of the food
        self.clock=pygame.time.Clock()
        # This clock is used to determine if the level is terminated
        self.clock2=pygame.time.Clock()
        
    
    def compute_level(self):
        
        i=0
        while self.level_time[i]<self.tps and i<len(self.level_time)-1:
            i+=1
        if self.niveau==i:
            self.niveau+=1
            for s in ecran.allScoudly:
                s.nb_anneaux+=1
                s.grandit()
        if self.niveau<9:
            self.timing=3000-ecran.niveau*300
        else:
            self.timing=400

    def timer(self,fps):
        self.game_timer+=self.clock.tick(fps)
        self.tps+=self.clock2.tick(fps)
        if self.power=="On" and self.power_timer<laps_power:
           self.power_timer+=self.clock3.tick(fps)
        elif self.power_timer>laps_power:
            self.power_timer=0
            self.power="Off"
            # Remove Serpent 2 et 3
            for s in self.allScoudly:
                if s.ind!=1:
                    self.allScoudly.remove(s)
                self.son01.set_volume(.8)
                self.son01.play()
        
    def update(self,rect):
        pygame.display.update(rect)
         
    def bandeau(self):
        
        # Le bandeau du Jeu
        font = pygame.font.Font(None, 24)           
        self.text1 = font.render("Level :" + str(self.niveau) , 1, bleu,noir)
        self.text1Rect=self.text1.get_rect()
        self.surface.blit(self.text1,self.text1Rect)
        
        self.text2 = font.render("Score :" + str(self.score) , 1, blanc,noir)
        self.text2Rect=self.text2.get_rect()
        self.text2Rect=self.text2Rect.move(100,0)
        self.surface.blit(self.text2,self.text2Rect)
        
        self.chrono=abs(int((self.tps-self.laps*self.niveau)/1000))
        self.text3 = font.render("Time :" + str(self.chrono) , 1, rouge,noir)
        self.text3Rect=self.text2.get_rect()
        self.text3Rect=self.text3Rect.move(220,0)
        self.surface.blit(self.text3,self.text3Rect)
        
        self.text4 = font.render("Power : " , 1, bleu,noir)
        self.text4Rect=self.text4.get_rect()
        self.text4Rect=self.text4Rect.move(310,0)
        self.surface.blit(self.text4,self.text4Rect) 
        
        if self.power=="Off":
            self.text5 = font.render(self.power , 1, bleu,noir)
        else:
            self.text5 = font.render(self.power , 1, orange,noir)
            
        self.text5Rect=self.text5.get_rect()
        self.text5Rect=self.text5Rect.move(self.text4Rect.right,0)
        self.surface.blit(self.text5,self.text5Rect) 
        self.update(self.text5Rect)
        
    ########################################################################
    #   The HighScore
    ########################################################################

    def raz(self):
        self.surface.blit(self.bg,self.bgRect)
        self.update(self.bgRect)
            
    def highscore_load(self):
     
        self.fichier_score=True
        try:
            fic=open("./high.txt","r")
        except:
            print ("Erreur ouverture hight.txt")
            self.fichier_score=False
        if self.fichier_score==True:
            eof=False
            while eof!=True:
                ligne=fic.readline()
                ligne=ligne[0:-1]
                if ligne=="":
                    eof=True
                else:
                    self.highscore.append([int(ligne.split(",")[0]),str(ligne.split(",")[1])])
            self.highscore.sort(reverse=True)
            self.highscore=self.highscore[0:5]
        else:
             self.highscore.append([0,"Scoudly"])
    
    def highscore_write(self):
        
        if self.fichier_score==True:
           fic=open("./high.txt","a")
        else:
           fic=open("./high.txt","w")
        self.raz()
        font=pygame.font.Font(None,24)  
        text1 = font.render("Score: " + str(self.score) + " || Nom / Name : ",1,vert,noir)
        text1Rect=text1.get_rect()
        text1Rect=text1Rect.move(int((self.size[0]-text1Rect.width)/2),200)
        self.surface.blit(text1,text1Rect)
        self.update(text1Rect)
        
        nom=""
        flag=True
        while flag==True:
            for e in pygame.event.get():
                if e.type==KEYDOWN:
                    
                    ### A-Z only
                   
                    if e.key>=97 and e.key<=122:
                        if len(nom)<8:
                            s=pygame.key.name(e.key)
                            nom+=s
                            text2 = font.render(nom,1,vert,rouge)
                            text2Rect=text2.get_rect()
                            text2Rect=text2Rect.move(text1Rect.right,200)
                            self.surface.blit(self.bg,text2Rect,text2Rect)
                            self.update(text2Rect)
                            self.surface.blit(text2,text2Rect)
                            self.update(text2Rect)
                    elif e.key==13:
                        flag=False
                    elif e.key==8:
                        self.surface.blit(self.bg,text2Rect,text2Rect)
                        nom=nom[0:len(nom)-1]
                        text2 = font.render(nom,1,vert,noir)
                        self.update(text2Rect)
                        self.surface.blit(text2,text2Rect)
                        self.update(text2Rect)
            pygame.time.wait(100)
        if len(nom)==0:
            nom="Scoudly"      
        fic.write(str(self.score)+","+str(nom)+"\n")
        fic.close
        
        
    def highscore_print(self):
        
        self.surface.blit(self.bg,self.bgRect)
        self.update(self.bgRect)
        font=pygame.font.Font(None,24)
        y=0  
        for score in self.highscore:
             text1 = font.render(str(score[0])+"  "+str(score[1]),1,jaune,noir)
             textpos = text1.get_rect()
             y=y+32
             textpos = textpos.move (int((self.size[0]-textpos.width)/2),264+y) 
             self.surface.blit(text1,textpos)
             self.update(textpos)

    def option_speed(self):
        font=pygame.font.Font(None,16)
        textOption = font.render("Vitesse / Speed : " + str(fps),1,jaune,noir)
        textOptionRect = textOption.get_rect()
        textOptionRect=textOptionRect.move((self.size[0]-textOptionRect.width)/2,0)

        self.surface.blit(textOption,textOptionRect)
        self.update(textOptionRect)
        
        textOption = font.render("<-- Key DOWN and Key UP -->" ,1,vert,noir)
        textOptionRect = textOption.get_rect()
        textOptionRect=textOptionRect.move((self.size[0]-textOptionRect.width)/2,textOptionRect.height)

        self.surface.blit(textOption,textOptionRect)
        self.update(textOptionRect)
                
    def menu(self):
        global fps
        self.choix=0
        self.bg2=pygame.image.load("./graph/menu.png")
        self.bgRect2=self.bg2.get_rect()
        self.surface.blit(self.bg2,self.bgRect2)
        self.update(self.bgRect2)
        self.cursorRect=self.cursorRect.move(320,148)
        self.surface.blit(self.cursor,self.cursorRect)
        self.update(self.cursorRect)
        while self.choix==0:
            pygame.time.wait(100)
            for e in pygame.event.get():
                if e.type==KEYDOWN:
                    
                    # Play / Jouer
                    if e.key==13 and self.cursorRect.top==148:
                         self.choix=1
                         
                    # Speed / Vitesse
                    elif e.key==13 and self.cursorRect.top==206:
                        self.make_clock()
                        while not pygame.key.get_pressed()[97] and not pygame.key.get_pressed()[113]:
                            ecran.timer(fps)
                            ecran.compute_level()
                            bg.update()
                            bg.draw(ecran.surface)
                            ecran.option_speed()
                            scoudly.affiche()
                            clavier()
                            pygame.event.get(KEYDOWN)
                            if pygame.key.get_pressed()[K_UP]:
                                fps+=1
                            elif pygame.key.get_pressed()[K_DOWN]:
                                fps-=1
                            pygame.display.flip()
                        self.surface.blit(self.bg2,self.bgRect2)
                        self.update(self.bgRect2)
                        
                    # Rules / Régles
                    
                    elif e.key==13 and self.cursorRect.top==322:
                        self.surface.blit(self.rule,self.ruleRect)
                        self.update(self.ruleRect)
                        while not pygame.key.get_pressed()[97] and not pygame.key.get_pressed()[113]:
                            wait(50)
                            pygame.event.get(KEYDOWN)
                            if pygame.key.get_pressed()[K_ESCAPE]:
                                sys.exit()
                        self.surface.blit(self.bg2,self.bgRect2)
                        self.update(self.bgRect2)
                        
                    # Highscore     
                    
                    elif e.key==13 and self.cursorRect.top==264:
                        self.highscore_print()            
                        while not pygame.key.get_pressed()[97] and not pygame.key.get_pressed()[113]:
                            wait(50)
                            pygame.event.get(KEYDOWN)
                            if pygame.key.get_pressed()[K_ESCAPE]:
                                sys.exit()
                        self.surface.blit(self.bg2,self.bgRect2)
                        self.update(self.bgRect2)
                        
                    # Down / Descendre   
                                            
                    elif e.key==K_DOWN and self.cursorRect.top<322:
                        self.surface.blit(self.bg2,self.cursorRect,self.cursorRect)
                        self.update(self.cursorRect)
                        self.cursorRect=self.cursorRect.move(0,58)
                        
                    # Up / monter
                    
                    elif e.key==K_UP and self.cursorRect.top>148:
                        self.surface.blit(self.bg2,self.cursorRect,self.cursorRect)
                        self.update(self.cursorRect)
                        self.cursorRect=self.cursorRect.move(0,-58)
                        
                    # Quit
                    
                    elif pygame.key.get_pressed()[97] or pygame.key.get_pressed()[113] or pygame.key.get_pressed()[K_ESCAPE]:
                        sys.exit()
                    self.surface.blit(self.cursor,self.cursorRect)
                    self.update(self.cursorRect)
                    
class Bg (pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("./graph/scroll.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Position initiale des deux images pour le scrolling continu
        self.y1 = 0
        self.y2 = -self.rect.height
        self.speed = 3  + ecran.niveau # Vitesse du scrolling (positive pour faire défiler vers le bas)
        
    def update(self):
        # Déplacement des deux images
        self.y1 += self.speed
        self.y2 += self.speed
        
        # Si une image sort de l'écran, elle est repositionnée au-dessus de l'autre
        if self.y1 >= self.rect.height:
            self.y1 = self.y2 - self.rect.height
        if self.y2 >= self.rect.height:
            self.y2 = self.y1 - self.rect.height
        
    def draw(self, Ecran):
        Ecran.blit(self.image, (0, self.y1))
        Ecran.blit(self.image, (0, self.y2))
    
class Food(pygame.sprite.Sprite):
    
    def __init__(self):
         
         pygame.sprite.Sprite.__init__(self)
         self.img=8*[""]      
         self.type=random.randint(0,7)
         
         self.img[0]="./graph/nuts.png"
         self.img[1]="./graph/ananas.png"
         self.img[2]="./graph/cerises.png"
         self.img[3]="./graph/banane.png"
         self.img[4]="./graph/pizza.png"
         self.img[5]="./graph/fraise.png"
         self.img[6]="./graph/poire.png"
         self.img[7]="./graph/pomme.png"
         self.image=pygame.image.load(self.img[self.type]).convert_alpha()
         self.rect=self.image.get_rect()
         self.rect.top=ecran.size[1]-(random.randint(0,50))
         self.rect.right=random.randint(self.rect.right,ecran.size[0])
         self.son01=pygame.mixer.Sound("./sound/hh_frappe1.wav")
         self.son02=pygame.mixer.Sound("./sound/ride_bell.wav")
         
    def update(self):
    
        if self.rect.top>12:
            self.rect.top-=4+ecran.niveau
            for snake in ecran.allScoudly:
                if snake.ind==1:
                    nb_anneaux=snake.nb_anneaux
                if self.rect.colliderect(snake.fond[0][1]):
                    ecran.score+=self.type+11
                    self.son01.set_volume(.8)
                    self.son01.play()
                    snake.score[0]=scoudly.score[1]
                    snake.score[1]=self.type+1
                    if snake.score[0]+snake.score[1]>=14: #ici 14
                        # Clock of power
                        ecran.clock3=pygame.time.Clock()
                        ecran.power_timer=0
                        ecran.power="On"
                        if len(ecran.allScoudly)==1:
                           
                            if snake.fond[0][1].left>0 and snake.fond[0][1].left<=32:
                                ecran.allScoudly.add(Scoudly(x=snake.fond[0][1].left+32,ind=2,nb_anneaux=nb_anneaux))
                            else:
                                ecran.allScoudly.add(Scoudly(x=snake.fond[0][1].left-32,ind=2,nb_anneaux=nb_anneaux))
                            
                        elif len(ecran.allScoudly)==2:
                          
                            posnew=0
                            for snake2 in ecran.allScoudly:
                                # Calcul où mettre le 3eme
                                if snake2.fond[0][1].left>posnew and snake2.fond[0][1].left<ecran.size[0]-32:
                                    posnew=snake2.fond[0][1].left + 32
                                else:
                                    posnew=snake2.fond[0][1].left - 32
                            ecran.allScoudly.add(Scoudly(x=posnew,ind=3,nb_anneaux=nb_anneaux))
                            
                            self.son02.set_volume(.5)
                            self.son02.play()
                    # Remove the food
                    self.kill()
        else:
            # Remove the food and decrease the score
            self.kill()
            ecran.score-=self.type+1
       

ecran=Ecran()
bg=Bg()
ecran.highscore_load()
scoudly=Scoudly(x=184,ind=1,nb_anneaux=5)

while True:
    ecran.menu()
    allfood = pygame.sprite.RenderUpdates()
    music_fond()
    ecran.make_clock()
    while ecran.niveau<=max_level and not pygame.key.get_pressed()[97] and not pygame.key.get_pressed()[113]:
        ecran.timer(fps)
        ecran.compute_level()
        bg.draw(ecran.surface)
        bg.update()
        ecran.bandeau()
        ecran.allScoudly.clear(ecran.surface,ecran.bg)
        ecran.allScoudly.draw(ecran.surface)
        ecran.allScoudly.update(0,"")
        if ecran.game_timer>ecran.timing:
            food=Food()
            allfood.add(food)
            ecran.game_timer=0
        allfood.update()
        allfood.draw(ecran.surface)
        pygame.display.flip()
        clavier()
    ecran.highscore_write()
    ecran.__init__()
    scoudly.__init__()
    ecran.highscore_load() 
