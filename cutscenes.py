#Cutscenes

import pygame
import time
from state import State


class Cutscene(State):
    #The cutscene class. It's interacted with more or less like a level without
    #input. That way the levels can link to it and it can link to levels
    #and maintain the order of the levels.

    #It functions based on how many animations it has. The cutscene ends when
    #you've seen all the animations.

    #Or you can skip it. But that's boring.

    #There's only one type of animation for now, but theoretically it would
    #work with any animation class I write.

    def __init__(self,game,changeBackground = None):
        self.game = game
        self.animations = []
        self.writingText = []
        self.index = 0
        self.background = changeBackground
        
        self.music = None
        self.image = None
        
    def loadImage(self, image):
        self.image = (pygame.image.load(image))


    def render(self):
        if self.image == None:
            self.image = pygame.Surface((self.game.width,self.game.height)).convert_alpha()
            self.image.fill(self.game.background.color)
        surface = pygame.transform.scale(self.image,
                                         (self.game.width,self.game.height))
        self.animations[self.index].draw(surface)
        return surface
        

    def update(self):
        #If the animation is complete, it moves to the next one.
        #If there are no more animations, move to the next level or cutscene.
        if self.game.state == self:
            if self.animations[self.index].update() == True:
                pass
            elif self.index<len(self.animations)-1:
                self.index+=1
            
            else:
                self.game.stateChange(self.game.levels[self.nextLevel])
            
            if self.background!=None:
                self.game.background = self.background

#lets you skip the cutscene
    def onMousePressed(self,event):
        self.game.stateChange(self.game.levels[self.nextLevel])
    def onKeyPressed(self,event):
        self.game.stateChange(self.game.levels[self.nextLevel])





    
class WritingText(object):
    #An animation class. It animates the text being written out on the
    #background image. Also has a time delay for timing!

    def __init__(self, text, pos, font, size, color, pause):
        self.text = text
        self.shownText = ""
        self.pos = pos
        self.font = pygame.font.SysFont(font,size,italic = True)
        self.color = color
        self.surface = self.font.render(self.shownText,True,color)
        self.rect = self.surface.get_rect(topleft = pos)
        self.pause = pause

    def draw(self,surface):
        surface.blit(self.surface,self.pos)


    def update(self):
        #on every update it moves one letter to what you see, then pauses.
        #if there are no more levels, it pauses, then moves on.
        if len(self.shownText) == len(self.text):
            time.sleep(self.pause)
            return False
        self.shownText = self.text[0:len(self.shownText)+1]
        self.surface = self.font.render(self.shownText,True,self.color)
        self.rect = self.surface.get_rect(topleft = self.pos)
        time.sleep(0.02)
        return True



