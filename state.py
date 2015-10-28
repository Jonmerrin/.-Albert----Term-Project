#State Class
import pygame,sys

class State(object):
    #Shell for any foreground state.

    def __init__(self):
        pass

    def onMouseMotion(self,event):
        pass

    def onMousePressed(self,event):
        pass

    def onMouseUp(self,event):
        pass

    
    def onKeyPressed(self,event):
        pass
    
    def update(self):
        pass

    def reset(self):
        pass
    



class PauseMenu(State):
    #The pause menu!
    
    #Keeps track of what the screen below it is, but stops it from updating.
    
    def __init__(self, width, height, surface, game, prevState):
        self.width,self.height = width, height
        self.surface,self.game,self.prevState = surface,game,prevState
        self.size = 12
        self.buttonHeight = 50
        self.buttonLen = 400
        green = (0,255,0)
        self.buttons = []
        
        self.menuRect = pygame.Rect((width/self.size,height/self.size),
                                    (width-2*width/self.size,
                                     (height-2*height/self.size)/2))
        self.menuRect.center = (self.width/2,self.height/2)

        
        #Continue Button
        self.continueText = "continue"
        self.continueSurface = self.game.font.render(self.continueText,
                                                     True,green)
        self.continueRect = pygame.Rect((self.menuRect.left+self.menuRect.width
                                         /self.size,
                                         self.menuRect.top+self.buttonHeight/2),
                                      (self.buttonLen,self.buttonHeight))
        self.buttons.append((self.continueText,self.continueSurface,
                             self.continueRect))

        #Reset Button
        self.resetText = "reset puzzle"
        self.resetSurface = self.game.font.render(self.resetText,
                                                     True,green)
        self.resetRect = pygame.Rect((self.menuRect.left+self.menuRect.width
                                     /self.size,
                                 self.continueRect.bottom+self.buttonHeight/2),
                                      (self.buttonLen,self.buttonHeight))
        self.buttons.append((self.resetText,self.resetSurface,self.resetRect))        



        #Main menu button
        self.quitText = "main menu"
        self.quitSurface = self.game.font.render(self.quitText,
                                                     True,green)
        self.quitRect = pygame.Rect((self.menuRect.left+self.menuRect.width
                                         /self.size,
                                     self.resetRect.bottom+self.buttonHeight/2),
                                      (self.buttonLen,self.buttonHeight))
        self.buttons.append((self.quitText,self.quitSurface,self.quitRect))


        #Exit Game button
        self.exitText = "exit game"
        self.exitSurface = self.game.font.render(self.exitText,
                                                     True,green)
        self.exitRect = pygame.Rect((self.menuRect.left+self.menuRect.width
                                         /self.size,
                                         self.quitRect.bottom+self.buttonHeight/2),
                                      (self.buttonLen,self.buttonHeight))
        self.buttons.append((self.exitText,self.exitSurface,self.exitRect))

        
        #Self.buttons keeps track of all the buttons and where they are.

    def render(self):
        surface = self.surface
        pygame.draw.rect(surface,pygame.Color(0,255,0),self.menuRect)
        pygame.draw.rect(surface,pygame.Color(0,50,0),self.continueRect)
        pygame.draw.rect(surface,pygame.Color(0,50,0),self.resetRect)
        pygame.draw.rect(surface,pygame.Color(0,50,0),self.quitRect)
        pygame.draw.rect(surface,pygame.Color(0,50,0),self.exitRect)
        

        for button in self.buttons:
            text,surf,rect = button
            surface.blit(surf,rect.topleft)

        return surface

    def onMousePressed(self,event):
        #Clicks a button!
        for button in self.buttons:
            text,surf,rect = button
            if rect.collidepoint(event.pos):
                self.activate_button(text)


    def onKeyPressed(self,event):
        #If you hit the pause button again, it goes back to the game.
        if event.key == 27:
            self.game.state = self.prevState

    def activate_button(self,name):

        #unpauses by going back to the previous state
        if name == "continue":
            self.game.state = self.prevState

        #resets the current puzzle    
        elif name == "reset puzzle":
            self.prevState.reset()
            self.game.state = self.prevState
        
        #goes to the main menu
        elif name == "main menu":
            self.game.stateChange(self.game.SplashScreen)
            with open("saveGame.txt","wt") as fout:
                fout.write(self.prevState.name+"\n"+self.game.background.name)

            
        #quits the game
        elif name == "exit game":
            with open("saveGame.txt","wt") as fout:
                fout.write(self.prevState.name+"\n"+self.game.background.name)
            pygame.quit()
            sys.exit()
