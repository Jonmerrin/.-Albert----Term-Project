#Level Building

import pygame
import math,random,copy
from state import *

class Level(State):
    

    #This is the level class. This is what the "state" of the game is going to
    #be. This will basically be a shell environment for the rest of the game.
    #Inside the concepts and associations will take most of the input,
    #with the level being a house for them.
    

    def __init__(self,width,height,game,depth):
        self.width,self.height,self.game = width,height,game
        self.concepts = []
        self.animations = []
        buttonWidth = 200
        buttonHeight = 50
        self.radius = 20
        self.nodeRadius = 10
        self.depth = self.initDepth = depth
        self.helpText = None
        self.defaultFont = "courier"
        self.fontSize = 30
        self.locked = False
        self.links = []
        self.color = (0,100,255)
        self.highlighted = (80,180,255)
        self.selected = None
        self.selectedLink = None
        self.complete = False
        self.music = None
        
        
        #The "solve" button
        self.buildButton = pygame.Rect((0,0),
                                       (buttonWidth,buttonHeight))
        self.buildButton.bottomleft = (buttonHeight,self.height-buttonHeight)
        self.buildText = "Compile"

        self.complete = False


    def render(self):
        #This is the render class. This works its way down from level to
        #level drawing the concepts, then the associations, then the nodes and
        #synapses.
        #The depth level will zoom in on a specific part of the puzzle
        
        
        if len(self.depth)==0:
            surface = pygame.Surface((self.width,self.height)).convert_alpha()
            surface.fill(pygame.Color(0,0,0,0))
            for concept in self.concepts:
                if concept==self.selected:
                    pygame.draw.circle(surface,self.highlighted,concept.pos,
                                   self.radius+len(self.links)*self.nodeRadius)
                else:
                    pygame.draw.circle(surface,self.color,concept.pos,
                                   self.radius+len(self.links)*self.nodeRadius)
            for link in self.links:
                link.draw(surface)
                
        else:
            surface = self.zoom(self.depth).render()


        #These are the things that will appear on every stage. A build button,
        #and the help text, if there is any.
        pygame.draw.rect(surface,(0,255,0),self.buildButton,4)
        text = pygame.font.SysFont(self.defaultFont,30)
        textSurface = text.render(self.zoom().buildText,True,(0,255,0))
        textBox = textSurface.get_rect(center = self.buildButton.center)
        surface.blit(textSurface,textBox.topleft)
        line_num = 2
        
        if self.zoom().helpText!=None:
            for line in self.zoom().helpText.splitlines():
                levelText = pygame.font.SysFont(self.defaultFont,self.fontSize)
                levelTextSurface = levelText.render(line,True,(0,255,0))
                levelTextBox = levelTextSurface.get_rect(
                    center = (self.width/2,self.fontSize*line_num))
                surface.blit(levelTextSurface,levelTextBox.topleft)
                line_num+=1
        
            
        return surface

    #####
    #Building functions. All contained within the level, which is the super-
    #wrapper. It'll be the state that the game interacts with.
    #####

    def createConcept(self,pos):
        #builds a new concepts object
        self.concepts.append(Concept(self.width,self.height,self.game,pos))

        

    def createAssociation(self,concept,pos):
        #builds a new association
        self.concepts[concept].associations.append(
            Association(self.width,self.height,self.game,pos))

        

    def createNode(self,nodeType,args,pos,connects,color = None):
        #builds a new node
        if color == None:
            self.zoom(args).nodes.append(
            nodeType(self.width,self.height,self.game,pos,connects))
        else:
            self.zoom(args).nodes.append(
            nodeType(self.width,self.height,self.game,pos,connects,color))


    #The zoom function is a sort of forced recursion down a path that the
    #game keeps track of. It lets me change the way input interacts with the
    #game and what is drawn and updated based on what you're looking at.
    #Zoom basically allows everything to work. All functions from here on
    #function based on zoom.
    def zoom(self, args=None):#              BEST FUNCTION EVER.
        if args == None: args = self.depth
        #follows the args (or "depth") 
        if len(args)==0:
            return self
        else: return self.concepts[args[0]].zoom(args[1:])

        

    def checkSolved(self):
        #checks if the outermost level is solved
        #if there are less than 2 concepts, that means it's not a concepts level
        #so it's already solved.
        if len(self.concepts)<2:
            self.complete = True
            return True
        
        for link in self.links:
            if link.linkedTo!=None:
                check = link.findPath(link.concept,[link])
                if check != None:
                    self.complete = True
                    return True
                
        return False

    
    
    def checkWin(self):
        #Checks if all the inner levels are solved. The inner levels check
        #if they are solved, and if all of their sub-levels are solved.
        
        for concept in self.concepts:
            if not(concept.checkWin()):
                return False
        if self.checkSolved():
            return True
        return False

    

    def update(self):
        #updates the screen you're looking at.
        if len(self.depth) == 0:pass
        else:
            self.zoom().update()
        if self.complete == True and len(self.zoom().animations) == 0:
            self.complete = False
            self.game.stateChange(self.game.levels[self.nextLevel])

    def onMousePressed(self,event):

        #Does the action for the build button for the current zoom
        if self.buildButton.collidepoint(event.pos):
            self.zoom().buildButtonPress()
            self.update()
            self.checkWin()
            
        #Base case for the zoom. If there's no depth, it does this:
        if len(self.depth)==0:
            x,y = event.pos
            
            #zooms in on a concept
            if event.button == 3:
                for concept in xrange(len(self.concepts)):
                    if self.concepts[concept].locked==False:
                        x2,y2 = self.concepts[concept].pos
                        radius = (self.radius+len(self.concepts[concept])
                                  *self.nodeRadius)
                        if (((x-x2)**2+(y-y2)**2)**0.5<=radius):
                            self.game.state.depth.append(concept)
                            self.game.updateAll()
                            
            #Lets you connect concepts based on rules defined below.
            elif event.button == 1:
                for link in self.links:
                    if (((x-link.pos1[0])**2+(y-link.pos1[1])**2)**0.5
                        <link.radius):
                        if link.linkedTo!=None:
                            link.linkedTo.linkedTo = None
                            link.linkedTo = None
                        link.bound1 = True
                    
                    elif (((x-link.pos2[0])**2+(y-link.pos2[1])**2)**0.5
                        <link.radius): 
                        if link.linkedTo!=None:
                            link.linkedTo.linkedTo = None
                            link.linkedTo = None
                            link.bound2 = True
                    
        #passes the event to the current zoom
        else: self.zoom().onMousePressed(event)

    def onMouseMotion(self,event):
        #Selects the concept and the node you're moused over
        if len(self.depth)==0:
            x,y = event.pos
            self.selected = None
            self.selectedLink = None
            for concept in xrange(len(self.concepts)):
                if self.concepts[concept].locked == False:
                    x2,y2 = self.concepts[concept].pos
                    radius = (self.radius+len(self.concepts[concept])
                              *self.nodeRadius)
                    if (((x-x2)**2+(y-y2)**2)**0.5<=radius):
                        self.selected = self.concepts[concept]
            for link in self.links:
                if (((x-link.pos1[0])**2+(y-link.pos1[1])**2)**0.5
                    <link.radius) or (((x-link.pos2[0])**2+(y-link.pos2[1])**2)
                                      **0.5<link.radius):
                    self.selectedLink = link

                    
        else:self.zoom().onMouseMotion(event)

    def onMouseUp(self,event):
        #Lets go of whatever you're holding. If you've made a link it checks
        #if it's legal.
        if len(self.depth)==0:
            x,y = event.pos
            for link in self.links:
                if link.bound1:
                    link.bound1 = False
                    if self.selectedLink != None:
                        link.link(self.selectedLink)
                elif link.bound2:
                    link.bound2 = False
                    if self.selectedLink != None:
                        link.link(self.selectedLink)


        else: self.zoom().onMouseUp(event)

    #Pause menu and temp change stage
    def onKeyPressed(self,event):
        if event.key == 27:
            self.game.state = PauseMenu(self.width,self.height,self.render(),
                                        self.game,self)
        #lets you zoom out
        elif event.key == 273:
            self.stageUp()

    #Checks if the level is solved
    def buildButtonPress(self):
        if self.checkSolved():
            self.complete = True

    #Goes up a "level" within the puzzle.
    #updates any information that might have changed on the lower level.
    def stageUp(self):
        if len(self.depth)!=0:
            if len(self.zoom().animations)==0:
                self.depth.pop()
                self.zoom().updateInfo()

    def updateInfo(self):
        #updates information changed when on a lower level
        self.links = []
        for concept in self.concepts:
            if concept.locked == False:
                concept.levelLinks = []
                for index in xrange(len(concept.path)):
                    dot = concept.path[index]
                    link = LevelLink(dot.nodes[0],dot.nodes[1],concept,index)
                    self.links.append(link)
                    concept.levelLinks.append(link)
            else:
                for link in concept.levelLinks:
                    self.links.append(link)

        
    #resets the puzzle
    def reset(self):
        newConcepts = []
        for concept in self.concepts:
            if concept.locked == False:
                concept.reset()
            newConcepts.append(concept)
        self.__init__(self.width,self.height,self.game,self.initDepth)
        for concept in newConcepts:
            self.concepts.append(concept)
            
#Sets up bounding boxes and whatnot for the level.
    def initialize(self):
        for concept in self.concepts:
            if concept.locked == False: #if it's locked, I don't want it to
                concept.updateInfo()    #change.
        self.updateInfo()

####################################################################
    #Concepts
####################################################################

class Concept(Level):

    #The middle level puzzle. Most of these are derivative of functions above.
    #I'll comment in the differences.

    def __init__(self,width,height,game,pos):
        self.width,self.height,self.game = width,height,game
        self.pos = pos
        self.path = []
        self.scale = 3
        self.associations = []
        self.associationBoxes = []
        self.levelLinks = []
        self.buildText = "CONSTRUCT" #CONSTRUCTOR
        self.helpText = None
        self.animations = []
        self.selected = None
        self.connectBoxes = []
        self.radius = 20
        self.locked = False
        

    def updateInfo(self):
        self.connectBoxes = []
        self.associationBoxes = []
        boxlen = 20
        for association in self.associations:
            association.connectBoxes = []
            association.update()
            tempBox = pygame.Rect((association.render().get_rect().topleft),
                          (self.width/len(self.associations),
                           self.height/len(self.associations)))

            tempBox.topleft = association.pos            
            self.associationBoxes.append(tempBox)
            if association.complete == True:
                for node in association.nodes:
                    for connection in node.connections:
                        if (type(connection.link)!=Synapse
                            and type(connection.node)!=Synapse
                            and connection.link!=None):
                            startx,starty = connection.node.pos
                            endx,endy = connection.link.pos
                            newPos = (association.pos[0]+((startx+endx)/2)
                                      /len(self.associations),
                                      association.pos[1]+((starty+endy)/2)
                                      /len(self.associations))
                            link = Link(newPos,self.game,association,
                                        connection.node,connection.link)
                            if not(link in self):
                                self.connectBoxes.append(link)
                                
                                association.connectBoxes.append(link)

            
    def update(self):pass
            

    def render(self):
        #Will render what's inside the concept. This will include all of the
        #associations, scaled to fit the screen.
        surface = pygame.Surface((self.width,self.height)).convert_alpha()
        surface.fill(pygame.Color(0,0,0,0))
        
        for association in self.associations:
            surface.blit(pygame.transform.scale(association.render().convert_alpha(),
                                                (self.width/
                                                 len(self.associations),
                                                 self.height/
                                                 len(self.associations))),
                         association.pos)
        for box in self.connectBoxes:
            box.draw(surface)
            if box == self.selected:
                pygame.draw.circle(surface,pygame.Color(255,255,0),box.pos,
                                   box.radius,1)
                                           
        return surface

    def checkSolved(self):
        if len(self.associations)<2:
            self.complete = True
            return True
        
        tempPath = []
        longestLoop = None
        for circle in self.connectBoxes:
            if circle.linkedTo!=None:
                tempPath = circle.findPath(circle.association,[circle])
                if longestLoop==None or len(tempPath)>len(longestLoop):
                    longestLoop = copy.copy(tempPath)
        if longestLoop!=None:
            self.path = longestLoop
            for circle in self.path:
                circle.color = pygame.Color(0,255,0)
                circle.linkedTo.color = pygame.Color(0,255,0)
            self.complete = True
            return True
            
        self.complete = False
        return False

            
    
    def checkWin(self):
        #Checks if the concept is solved and if all of the associations are
        #solved.
        for association in self.associations:
            if not(association.complete):
                return False
        if self.checkSolved():
            return True
        return False

    
    def zoom(self,args):
        #zooms in on a lower function. To be called by the higher zoom.
        if len(args)==0:
            return self
        else: return self.associations[args[0]].zoom(args[1:])

        #See? It comes in handy.


    def onMouseMotion(self,event):
        #Selects an a connectBox.
        x,y = event.pos
        
        for circle in self.connectBoxes:
            if ((x-circle.pos[0])**2+(y-circle.pos[1])**2)**0.5<=circle.radius:
                self.selected = circle
                return
            else:
                self.selected = None

    def onMousePressed(self,event):
        if event.button == 3:
            for box in xrange(len(self.associationBoxes)):
                if self.associationBoxes[box].collidepoint(event.pos):
                    if self.associations[box].locked==False:
                        self.game.state.depth.append(box)
                        self.game.updateAll()
        elif event.button == 1:
            if self.selected!=None:
                self.complete = False
                for circle in self.path:
                    circle.color = pygame.Color(255,0,0)
                    circle.linkedTo.color = pygame.Color(255,0,0)
                self.path = []
                self.selected.bound = True
                if self.selected.linkedTo!=None:
                    self.selected.linkedTo.linkedTo = None
                    self.selected.linkedTo = None
                
                
    
                    
                    
    def onMouseUp(self,event):
        for circle in self.connectBoxes:
            if circle.bound:
                circle.bound = False
                if self.selected!=None:
                    circle.link(self.selected)
                    
                    
    
    def onKeyPressed(self,event):
        pass

    
    def buildButtonPress(self):
        if self.checkSolved():
            self.complete = True


    #Continues reset
    def reset(self):
        newAssociations = []
        for association in self.associations:
            association.reset()
            newAssociations.append(association)
        self.__init__(self.width,self.height,self.game,self.pos)
        for association in newAssociations:
            self.associations.append(association)



    def __contains__(self,arg):
        for box in self.connectBoxes:
            if arg == box:
                return True
        for link in self.levelLinks:
            if arg  == link:
                return True
    def __len__(self):
        return len(self.path)

            
####################################################################
    #Associations
####################################################################

class Association(Level):

    #Bottom level puzzle. Again, mostly the same.

    def __init__(self,width,height,game,pos): #positions are important!
        self.width,self.height,self.game,self.pos = width,height,game,pos
        self.initPos = pos
        self.nodes = []
        self.animations = []
        self.connectBoxes = []
        self.buildText = "FIRE"
        self.helpText = None
        self.complete = False
        self.locked = False

    def update(self):
        for node in self.nodes:
            node.update()

            #Animation for the pulses, and adding and deleting as necessary.
        for pulse in self.animations:
            if pulse.moves>self.game.fps:
                self.animations.remove(pulse)
                if type(pulse.node2)!=Synapse:
                    for connection in pulse.node2.connections:
                        if (not(connection.link is pulse.node1) and
                            not(connection.link is pulse.node2)):
                            if not(connection.link in pulse.path):
                                self.animations.append(
                                Pulse(pulse.node2,connection.link,
                                      pulse.path+[pulse.node2]))
                        elif (not(connection.node is pulse.node1)
                            and not(connection.node is pulse.node2)):
                            if not(connection.node in pulse.path):
                                self.animations.append(
                                    Pulse(pulse.node2,connection.node,
                                      pulse.path+[pulse.node2]))
                del pulse
            else: pulse.update()
        
    def render(self):
        #Renders the association by drawing all the nodes.
        surface = pygame.Surface((self.width,self.height)).convert_alpha()
        surface.fill(pygame.Color(0,0,0,0))
        for node in self.nodes:
            node.draw(surface)
        for animation in self.animations:
            animation.draw(surface)
        return surface


    def checkSolved(self):
        #checks if the association is solved by checking if all the nodes
        #are in order.
        for node in self.nodes:
            if type(node) == Synapse:
                for connection in node.connections: #starts animation
                    self.animations.append(Pulse(node,connection.link,[node]))
                    
                if node.fire([node])==False:
                    return False
        
        return True
                

    def checkWin(self):
        return self.complete

    
    def zoom(self,arg):
        #zooms in on a particular node. Only meant to be called by a higher
        #zoom function when necessary.
        if len(arg)==0:
            return self
        else: return self.nodes[arg[0]]

        #*breathes on hand* *rubs on shirt*

    def onMousePressed(self,event):
        #Checks if you're clicking close enough to a connector
        x,y = event.pos
        buttonR = 10
        for node in self.nodes:
            for connection in node.connections:
                if((x-connection.dest[0])**2+
                   (y-connection.dest[1])**2)**0.5<=buttonR:
                    if connection.locked == False:
                        connection.bound=True
                        self.complete = False
                        self.connectBoxes  = []
                
    def onMouseUp(self,event):
        #finalizes connections between nodes, if legal
        for node in self.nodes:
            for connection in node.connections:
                if connection.bound:
                    for node in self.nodes:
                        if (((connection.dest[0]-node.pos[0])**2
                            +(connection.dest[1]-node.pos[1])**2)**0.5
                            <node.radius) and node!=connection.node:
                            if connection.makeLink(node):
                                node.connections.append(connection)
                            break
                        elif(connection.link!=None):
                            connection.link.connections.remove(connection)
                            connection.link = None
                    connection.bound=False

    def onMouseMotion(self,event):
        #Drags around the connections
        for node in self.nodes:
            for connection in node.connections:
                if connection.bound:
                    connection.dest = event.pos


    def buildButtonPress(self):
        if(self.checkSolved()):
            self.complete = True

    #continues the reset
    def reset(self):
        newNodes = []
        for node in self.nodes:
            node.reset()
            newNodes.append(node)
        self.__init__(self.width,self.height,self.game,self.pos)
        for node in newNodes:
            self.nodes.append(node)


####################################################################
    #Nodes
####################################################################

class Node(State):
    #Building blocks for the bottom level puzzle

    def __init__(self,width,height,game,pos,connects,color=(0,0,255),radius=10):
        self.width,self.height,self.game = width,height,game
        self.pos,self.radius = pos,radius
        self.color = color
        self.connects = connects
        self.connections = []
        self.locked = True
        for connection in xrange(connects):
            self.connections.append(Connection(self))

    def update(self):
        for connection in self.connections:
            connection.update()

    def render(self):
        #This catches the render if the zoom somehow goes too far.
        self.game.state.depth.pop()
        return self.game.state.zoom().render()

    def fire(self,alreadyChecked):
        #This is the checkWin. It recursively checks the connections
        #To make sure they all lead to synapses. If there are dead ends, it
        #returns false.

        if not(self in alreadyChecked):
            if type(self)==Synapse: pass
            elif  len(self.connections)<=1: return False
            alreadyChecked.append(self)
            for connection in self.connections:
                if connection.link==None:
                    return False
                if self == connection.node:
                    a = connection.link.fire(alreadyChecked)
                else: a = connection.node.fire(alreadyChecked)

                if a == False:
                    return a
        else: #Base case. For start up.
            if type(self) == Synapse:
                for connection in self.connections:
                    if connection.link==None:
                        return False
                    if self == connection.node:
                        a = connection.link.fire(alreadyChecked)
                    else: a = connection.node.fire(alreadyChecked)
                    if a == False:
                        return a
                    
        return True

    def draw(self,surface):
        #draws the nodes
        x,y = self.pos
        x-=self.radius/2
        y-=self.radius/2
        pygame.draw.circle(surface,self.color,self.pos,self.radius)
        
        for connection in self.connections:
            connection.draw(surface)


    #completes the reset
    def reset(self):
        for connection in self.connections:
            del connection
        self.__init__(self.width,self.height,self.game,self.pos,
                      self.connects,self.color,self.radius)




####################################################################
    #Synapses
####################################################################

#A type of node.

class Synapse(Node):
    def __init__(self,width,height,game,pos,connects = 2,name = "synapse",
                 radius=20):

        super(Synapse,self).__init__(width,height,game,pos,connects,name,
                                     radius)
        self.color = pygame.Color(20,240,55)


####################################################################
    #Connections
####################################################################

class Connection(object):
    #Connection class. Checks if a connection is legal, and is used a lot
    #in the higher level puzzles.
    def __init__(self,node,length = 100):
        self.width,self.height,self.game = node.width,node.height,node.game
        self.node,self.pos = node,node.pos
        self.length = length
        direction = random.random()*2*math.pi
        self.dest = self.origin = (int(self.pos[0]+math.cos(direction)*length),
                                   int(self.pos[1]+math.sin(direction)*length))
        #Sets the position randomly and forces it to be on the screen.
        #Mostly so I don't have to manually set all of the connection positions.
        while not(pygame.Rect((0,0),(self.width,self.height)).collidepoint(
            self.dest)):
            direction = random.random()*2*math.pi
            self.dest = self.origin = (
                int(self.pos[0]+math.cos(direction)*length),
                int(self.pos[1]+math.sin(direction)*length))
        self.bound = False
        self.link = None
        self.locked = False

    def makeLink(self,node):
        #Checks if the links are legal. If it's not the same type of node or
        #itself, it's legal.
        for connection in node.connections:
            if connection.link == self.node and connection.node ==node:
                return False
            elif connection.link == node and connection.node == self.node:
                return False
        if self.node.color==node.color:
            return False
        if type(node)==Synapse: return False
        else:
            self.dest = node.pos
            self.link = node
            return True
        
            

    def draw(self,surface):
        pygame.draw.line(surface,(255,255,255), self.pos,self.dest,3)
        if self.link == None:
            pygame.draw.circle(surface,pygame.Color(255,255,255,200),
                               self.dest,5)
        
    def update(self):
        #moves the connections back to their original positions.
        if not(self.bound) and self.link==None:
            if self.dest!=self.origin:
                destX,destY = self.dest
                originX,originY = self.origin
                self.dest = ((destX+originX)/2,(destY+originY)/2)
                

####################################################################
    #Pulse
####################################################################


class Pulse(object):
    #The class for the pulse animation.
    
    def __init__(self,node1,node2,path):
        self.node1,self.node2 = node1,node2
        self.pos = node1.pos
        self.path = path
        if node2==None:
            self.node2 = Node(node1.width,node1.height,node1.game,node1.pos,0)
        self.end = self.node2.pos
        
        self.trail = self.pos
        x1,y1 = self.pos
        x2,y2 = self.end
        (self.dx,self.dy)=(((x2-x1)*1.0)/node1.game.fps,
                           ((y2-y1)*1.0)/node1.game.fps)
        self.trailLen = 20
        self.moves = 0
        self.pulseSize = 12
        self.drawRect = pygame.Rect(self.pos,(self.trailLen,self.pulseSize))
        

    def update(self):
        (x,y) = self.pos
        x2,y2 = self.end
        x3,y3 = self.drawRect.center
        self.trail = (x-self.dx,y-self.dy)
        self.pos = (x+self.dx,y+self.dy)
        self.drawRect.center = x3+self.dx,y3+self.dy
        
        self.moves+=1
        
    def draw(self,surface):
        pygame.draw.line(surface,pygame.Color(200,200,60),self.trail,self.pos,
                         self.pulseSize)
         



####################################################################
    #Links
####################################################################


class Link(object):
    #Middle puzzle connectors. A bit more sophisticated than connections.
    #These use the lower level connections as their attributes and link
    #Together based on those.
    def __init__(self, pos, game,association,node1,node2):
        self.pos,self.game = pos, game
        self.radius = 5
        self.locked = False
        self.nodes = (node1,node2)
        self.association = association
        self.linkedTo = None
        self.bound = False
        self.color = pygame.Color(255,100,100,100)

    def draw(self,surface):
        pygame.draw.circle(surface,self.color,self.pos,self.radius)
        if self.linkedTo != None:
            pygame.draw.line(surface,self.color,self.pos,self.linkedTo.pos)
        if self.bound == True:
            pygame.draw.line(surface,pygame.Color(0,100,255,50),self.pos,
                             pygame.mouse.get_pos(),3)


    def link(self, other):
        #Makes sure the link follows the rules of the puzzle, then
        #makes the link. If the nodes making the connection are the same,
        #The links match up.
        if other.linkedTo==None:
            if other.association != self.association:
                if (self.nodes[0].color==other.nodes[0].color
                    and self.nodes[1].color==other.nodes[1].color):
                    self.linkedTo = other
                    other.linkedTo = self
                elif (self.nodes[1].color == other.nodes[0].color
                      and self.nodes[0].color==other.nodes[1].color):
                    self.linkedTo = other
                    other.linkedTo = self

        
            
            

        
    def update(self):pass #no need.


    def findPath(self,start,alreadyChecked):
        #Recursively finds the closed circuit that solves the puzzle.
        for circle in self.linkedTo.association.connectBoxes:
            if circle.linkedTo!=None:
                newChecked = alreadyChecked+[circle]
                if (circle in alreadyChecked
                    or circle.linkedTo in alreadyChecked):
                    continue
                elif circle.linkedTo.association == start:
                    return newChecked
                else:
                    a = circle.findPath(start,newChecked)
                    if a != None:
                        return a
        return None        


    def __eq__(self,other):
        #I use this in findPath to find if you are where you started.
        if type(other)!=type(self): return False

        if self.pos == other.pos:
           return True
        return False


####################################################################
    #LevelLinks
####################################################################

    
class LevelLink(object):

    #The links between the concepts for the outer level. Or "Level Links"
    #These connect based on what links were used to form the concept.

    def __init__(self,node1,node2,concept,number):
        self.concept = concept
        self.pos = concept.pos
        self.node1,self.node2 = node1,node2
        self.radius = 10
        self.line = 5
        self.size  = len(concept)
        x,y = self.pos
        self.pos1 = (x-concept.radius,y-(self.size/2-number)*2*self.radius)
        self.pos2 = (x+concept.radius,y-(self.size/2-number)*2*self.radius)
        self.linkedTo = None
        self.bound1 = False
        self.bound2 = False

    def draw(self,surface):
        #Draws the concepts with varying size based on how many links they have.
        #Also draws a representation of their links in order on the screen.
        #Only the links used in the path are recorded.
        x,y = self.pos
        pygame.draw.line(surface,(100,100,100),self.pos1,self.pos2,self.line)
        pygame.draw.circle(surface,self.node1.color,
                           (self.pos1),self.radius)
        pygame.draw.circle(surface,self.node2.color,
                           (self.pos2),self.radius)

        if self.linkedTo!=None:
            pygame.draw.line(surface,pygame.Color(255,255,255,50),
                             self.pos1,self.linkedTo.pos1)
            pygame.draw.line(surface,pygame.Color(255,255,255,50),
                             self.pos2,self.linkedTo.pos2)

        if self.bound1 != False:
            pygame.draw.line(surface,pygame.Color(0,100,255,50),self.pos1,
                             pygame.mouse.get_pos(),3)
        if self.bound2 != False:
            pygame.draw.line(surface,pygame.Color(0,100,255,50),self.pos2,
                             pygame.mouse.get_pos(),3)


    def findPath(self,start,alreadyChecked):
        #Checks if you win. It more or less works the same way as the
        #Middle level, but is a little cleaner and uses different criteria for
        #the links.


        for link in self.linkedTo.concept.levelLinks:
            if link.linkedTo!=None and link.linkedTo!=self:
                newChecked = alreadyChecked+[link]
                if (link in alreadyChecked
                    or link.linkedTo in alreadyChecked):
                    continue
                elif link.linkedTo.concept == start:
                    return newChecked
                else:
                    a = link.findPath(start,newChecked)
                    if a !=None: return a
        return None


    def link(self,other):
        #makes sure the link is legal. If the entire link is in the other
        #concept or if the two links have nothing in common, the link won't work
        if not(self in other.concept):
            if (self.node1.color == other.node1.color
                or self.node1.color == other.node2.color
                or self.node2.color == other.node1.color
                or self.node2.color == other.node2.color):

                self.linkedTo = other
                other.linkedTo = self
                

    def __eq__(self,other):
        #Used to check if the links are the same.
        if type(other)!=type(self):return False
        if (self.node1.color == other.node1.color
            and self.node2.color == other.node2.color):
            return True
        elif (self.node1.color == other.node2.color
              and self.node2.color == other.node1.color):
            return True
        else: return False

                 
