#WOOF

import pygame,sys,random,os
from pygame.locals import *
from puzzleParts import *
from state import State
from levels import *


#Credit where credit is due: Music by Kan R. Gao and Jim Guthrie, legally
#purchased through humble bundle. Sound effects are just shortened versions of
#their tracks.

##############################################################
            #Game
##############################################################

class Game(object):
    #The game class. This is kind of the wrapper class for the whole game.
    #It contains a background, a foreground that accepts the user input,
    #and it updates everything.
    def __init__(self, width = 750, height = 750):
        self._running = True
        pygame.init()
        self.fps = 30
        self.fpsClock = pygame.time.Clock()
        self.width,self.height = width,height

        #Sets up the display. DISPLAYSURF seemed to be conventional for pygame.
        self.DISPLAYSURF = pygame.display.set_mode((width,height))
        self.font = pygame.font.SysFont("courier",30)
        pygame.display.set_caption("Albert")

        #Sets up the backgrounds, main menu, transitions and levels
        self.background1 = Background1(self.width,self.height)
        self.background2 = Background2(self.width,self.height)
        self.background = self.background1
        self.backgroundColor = (0,50,0)
        self.SplashScreen = SplashScreen(self.width,self.height,self)
        self.state = self.SplashScreen
        self.filter = FadeFilter(self)
        levelList = LevelWrapper(self.width,self.height,self)
        self.levels = levelList.import_levels()

        if os.path.exists("saveGame.txt"):
            with open("saveGame.txt","rt") as fin:
                step = fin.read()
                step = step.splitlines()[1]
                if step == "background1": pass
                elif step == "background2":
                    self.background= self.background2
                    
                
        


    def drawAll(self):
        #Draws the background and the foreground.
        
        self.DISPLAYSURF.fill(self.backgroundColor)
        self.DISPLAYSURF.blit(self.background.render(),(0,0))
        self.DISPLAYSURF.blit(self.state.render(),(0,0))
        pygame.display.update()


    def stateChange(self, newState):
        #Changes to a new state. With transitions!
        #Tranisitions the music too, if there's a music change.

        self.filter.prevState = self.filter.curState = self.state
        self.filter.nextState = newState
        self.state = self.filter
        if newState.music!=None:
            pygame.mixer.music.load(newState.music)
            pygame.mixer.music.play(-1,0)
        self.drawAll()

        
        

    def resolveEvent(self,events):
        #Passes the event into the state. The event is resolved there.
        
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.state.onMousePressed(event)
            elif event.type == MOUSEBUTTONUP:
                self.state.onMouseUp(event)
            elif event.type == MOUSEMOTION:
                self.state.onMouseMotion(event)
            elif event.type == KEYDOWN:
                self.state.onKeyPressed(event)
                

    def updateAll(self):
        #Yup, that's it. Update all updates the background and the foreground.
        
        self.background.update()
        self.state.update()
        

        

    def gameLoop(self):
        #This is where the magic happens. FPS is set to 30 frames per second,
        #and it draws, resolves event, updates, and repeats.
        
        while self._running:
            self.drawAll()
            self.resolveEvent(pygame.event.get())
            self.fpsClock.tick(self.fps)
            self.updateAll()


    def run(self):
        self.gameLoop()




##############################################################
            #Background1
##############################################################
        
class Background1(object):
    #The first of hopefully many backgrounds. For this project, there
    #will be 2, for proof of concept.

    #separating the background and the foreground just lets me edit them
    #independently in game.
    
    def __init__(self,width,height):
        self.width,self.height = width,height
        self.static = []
        self.color = pygame.Color(0,50,0)
        self.name = "background1"

    def render(self):
        #Draws the background color, followed by static if there is any.
        surface = pygame.Surface((self.width,self.height)).convert_alpha()
        surface.fill(self.color)
        for roll in self.static:
            if roll.pos>=self.height:
                self.static.remove(roll)
                del roll
            else:
                roll.draw(surface)
        return surface
    
    def rand(self):
        #Performs actions based on probability. In the backgrounds, this causes
        #the static to roll.

        #random thickness, random intervals.
        staticProb = 350
            
        if random.randint(0,staticProb) == staticProb:
            self.static.append(StaticRoll(self.width,self.height))

    def update(self):
        #Makes new static and moves the static that's on the screen
        self.rand()
        for roll in self.static:
            roll.update()




##############################################################
            #Background2
##############################################################
        
class Background2(object):
    #The second of hopefully many backgrounds. More or less like the first one,
    #but uses an image as the background rather than a color.
    
    def __init__(self,width,height):
        self.width,self.height = width,height
        self.static = []
        self.color = pygame.Color(0,50,0)
        self.image = pygame.image.load("drawing.png")
        self.name = "background2"

    def render(self):
        #uses the image as the surface, scales it to fit the screen, then
        #draws the static.
        
        background = pygame.transform.scale(self.image,(self.width,self.height))
        surface = background.convert_alpha()
        for roll in self.static:
            if roll.pos>=self.height:
                self.static.remove(roll)
                del roll
            else:
                roll.draw(surface)
        return surface
    
    def rand(self):
        #same random as before
        staticProb = 350
            
        if random.randint(0,staticProb) == staticProb:
            self.static.append(StaticRoll(self.width,self.height))

    def update(self):
        #same update as before
        self.rand()
        for roll in self.static:
            roll.update()
            




#Static Roll for background 1
    
class StaticRoll(object):
    #That famous static roll.
    #Like the electric slide, but makes your hair stand up.


    def __init__(self,width,height):
        
        self.width,self.height = width,height
        self.pos = 0
        self.staticSize = 2
        self.staticHeight = random.randint(1,4) #random height
        self.static = []

    def update(self):
        #Moves the static downward and shuffles the image.
        #If it goes off the screen, it is deleted.
        self.pos+=self.staticSize*2
        if len(self.static)>self.staticHeight:
            self.static.pop(0)
        a = []
        for box in xrange(self.width/self.staticSize):
            a.append(random.randint(0,180))
        self.static.append(a)
        for row in self.static:
            random.shuffle(row)

    def draw(self,surface):
        for row in xrange(len(self.static)):
            for box in xrange(len(self.static[row])):
                shade= pygame.Color(255,255,255,self.static[row][box])
                pygame.draw.rect(surface, shade,(self.staticSize*box,
                                    self.pos+row*self.staticSize,
                                    self.staticSize,self.staticSize))

        
##############################################################
            #SplashScreen
##############################################################
            
class SplashScreen(State):
    #The title page and main menu.

    def __init__(self, width, height, game):
        self.width,self.height = width,height
        self.font = 'courier'
        initSize = 32
        self.titleSize = 100
        self.margin = 200
        self.game = game
        
        #The first second of Trailer Theme - 1 by Koji Kondo
        self.music = "beep.wav"
        pygame.mixer.music.load("beep.wav")
        pygame.mixer.music.play(-1)

        
        #title
        self.titleText = './Albert'
        self.title = pygame.font.SysFont(self.font,initSize)
        self.titleSurface = self.title.render(self.titleText, True, (0,255,0))        
        self.titleRect = self.titleSurface.get_rect()
        self.titleRect.center = (self.margin/2,self.margin/2)

        #play game button
        self.playText = 'PLAY_GAME'
        self.play = pygame.font.SysFont(self.font,initSize)
        self.playSurface = self.play.render(self.playText,True,(0,255,0))
        self.playButton = self.playSurface.get_rect()
        self.playButton.center = (self.margin,self.height-self.margin)

        #load game button
        self.loadText = 'LOAD_GAME'
        self.load = pygame.font.SysFont(self.font,initSize)
        self.loadSurface = self.load.render(self.loadText,True,(0,255,0))
        self.loadButton = self.loadSurface.get_rect()
        self.loadButton.center = (self.width-self.margin,
                                  self.height-self.margin)

        #Changes how the title page looks depending on whether or not
        #the user has played before.
        if os.path.exists("saveGame.txt"):
            self.titleText = random.choice(['"Hello Professor"',
                                            '"How are you today?"',
                                            '"Welcome back"',
                                            '"Ready to learn?"',
                                            '"Good to see you"'])
            self.titleSize = 60


        
        #These lists keep track of all the text.
        #I'll use this for the "glitches" later.
        self.text = [(self.title,self.titleSurface,
                      self.titleText,self.titleSize),
                     (self.play,self.playSurface,
                      self.playText,initSize),
                     (self.load,self.loadSurface,
                      self.loadText,initSize)]
        self.posit = [self.titleRect,self.playButton,self.loadButton]

        #Again, changes the way the main menu looks if you've played before.
        if os.path.exists("saveGame.txt"):
            self.messageText = './Albert'
            self.message = pygame.font.SysFont(self.font,initSize/2)
            self.messageSurface = self.load.render(self.loadText,True,(0,255,0),
                                                   True)
            self.messageRect = self.loadSurface.get_rect()
            self.messageRect.topleft = (self.titleRect.left,
                                       self.titleRect.bottom-initSize*2)
            self.text.append((self.message,self.messageSurface,
                              self.messageText,initSize/2))
            self.posit.append(self.messageRect)
            


    def render(self):
        #draws all the words as they appear in the list.

        surface = pygame.Surface((self.width,self.height)).convert_alpha()
        surface.fill(pygame.Color(0,0,0,0))
        
        for words in xrange(len(self.text)):
            font,surf,text,size = self.text[words]
            pos = self.posit[words]
            surface.blit(surf,pos)

        return surface

    def rand(self):
        #a wrapper for the random action.
        aProb = 25
        self.glitch(aProb)
            

    
    def glitch(self, prob):
        #randomly switches the size and italicization (it's a word)
        #of all the text on the screen to simulate glitching.
        
        #Any additional glitches are purely features, I promise.
        
        if (random.randint(0,prob)==prob):
            for element in xrange(len(self.text)):
                obj,surf,text,size = self.text[element]
                obj = pygame.font.SysFont(self.font,size+18)
                obj.set_italic(True)
                surf = obj.render(text,True,(0,255,0))
                self.text[element] = (obj,surf,text,size)

        else:
            for element in xrange(len(self.text)):
                obj,surf,text,size = self.text[element]
                obj = pygame.font.SysFont(self.font,size)
                obj.set_italic(False)
                surf = obj.render(text,True,(0,255,0))
                self.text[element] = (obj,surf,text,size)


    
    def update(self):
        self.rand()

    def onMousePressed(self,event):
        #play button! If there's no savefile, it makes one.
        
        if self.playButton.collidepoint(event.pos):
            self.game.stateChange(self.game.levels["opening_sequence1"])
            self.game.background = self.game.background1
            with open("saveGame.txt","wt") as fout:
                fout.write("level1\nbackground1")

        #load button! Switches the music to be the game music.
        elif self.loadButton.collidepoint(event.pos):
            if os.path.exists("saveGame.txt"):
                with open("saveGame.txt","rt") as fin:
                    level = fin.read().splitlines()[0]
                    
                self.game.levels[level].music = ("16 Cabin Music (Bonus Track).mp3")
                

                self.game.stateChange(self.game.levels[level])
                
    



    def reset(self):
        
        self.__init__(self.width,self.height,self.game)



class FadeFilter(State):
    #TRANSITIONS!!!!

    #This class lets you fade transition from foreground to foreground.

    def __init__(self,game):
        self.game = game
        self.prevState = self.nextState = self.curState = None
        self.alpha = 0
        self.gradientShift = 20
        self.fade = True

    def render(self):
        surface = pygame.Surface((self.game.width,self.game.height)).convert_alpha()
        surface.fill(pygame.Color(0,0,0,self.alpha))
        newSurf = self.curState.render()
        newSurf.blit(surface,(0,0))
        return newSurf

    def update(self):
        #If the fade is false, it fades out. Once it's fully faded out,
        #fade becomes true and it fades in.
        #Once it's fully faded in, it passes into the next foreground.
        
        if self.fade == False:
            if self.alpha-self.gradientShift<=0:
                self.alpha = 0
                self.game.state = self.nextState
                self.fade = True
            else: self.alpha-=self.gradientShift
        else:
            if self.alpha+self.gradientShift>=255:
                self.alpha = 255
                self.curState = self.nextState
                
                self.prevState.reset()
                self.fade = False
            else: self.alpha+=self.gradientShift





if __name__ == "__main__":
    
    a = Game()    
    a.run()
