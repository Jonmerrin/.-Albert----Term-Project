#List of Levels:

from puzzleParts import *
from cutscenes import *


class LevelWrapper(object):
#The wrapper for all the levels. This is how I initialize the levels, then
#funnel the dictionary into the main game. This dictionary also holds the
#cutscenes

    def __init__(self, width, height,game):
        self.width,self.height = width,height
        levels = dict()

        #The color dictionary makes my life easier when writing the levels
        colors = dict()
        colors["A"] = (0,0,255)
        colors["B"] = (255,0,0)
        colors["C"] = (0,255,255)
        colors["D"] = (255,0,255)
        colors["F"] = (100,100,100)
        
############################
#Structure for a level:
#Add in a concept
#Add in an association
#Add in the nodes for the level
#If there should be more associations in the level, add another and add nodes.
#If there should be more concepts in the level, add another and add associations

#end on adding the level name, help text, and the next level so it has an order.
#Some levels have music built in. This is for transitioning purposes, if, say,
#a cutscene has different music from the game. It lets me switch between them.
###########################


#Level One Test Code
        levels['level1'] = Level(self.width,self.height,game,[0,0])
        levels['level1'].createConcept((self.width/2,self.height/2))
        levels['level1'].createAssociation(0,(self.width/2,self.height/2))
        levels['level1'].createNode(Synapse,[0,0],(50,self.height/2),1)
        levels['level1'].createNode(Node,[0,0],(self.width/2,self.height/2),0)
        levels['level1'].createNode(Synapse,[0,0],(self.width-50,self.height/2),
                                    1)
        levels['level1'].zoom([0,0]).helpText = "The big circles are Synapses\
 and the\nsmaller ones are nodes. Connect\nSynapses to make associations and \
learn!\n\nDrag the ends of the connections\n to connect the nodes and hit fire!"
        #Music by Jim Guthrie
        levels['level1'].music = "16 Cabin Music (Bonus Track).mp3"
        
        levels['level1'].nextLevel = "level2"
        levels['level1'].name = "level1"
        levels['level1'].initialize()



#Level Two Test Code
        levels['level2'] = Level(self.width,self.height,game,[0,0])
        levels['level2'].createConcept((self.width/2,self.height/2))
        levels['level2'].createAssociation(0,(self.width/2,self.height/2))
        levels['level2'].createNode(Synapse,[0,0],(50,self.width/2),1)
        levels['level2'].createNode(Node,[0,0],(self.width/2,self.width/2),0,
                               colors["A"])
        levels['level2'].createNode(Node,[0,0],(self.width/2,self.height/2+200),
                                    1,colors["B"])
        levels['level2'].zoom().nodes[2].connections[0].makeLink(
            levels['level2'].zoom().nodes[1])
        levels['level2'].zoom().nodes[2].connections[0].dest = (
            levels['level2'].zoom().nodes[1].pos)
        levels['level2'].zoom().nodes[2].connections[0].locked = True
        levels['level2'].zoom().nodes[1].connections.append(
            levels['level2'].zoom().nodes[2].connections[0])
        
        levels['level2'].createNode(Synapse,[0,0],(self.width-50,self.width/2),2)
        levels['level2'].nextLevel = "level3"
        levels['level2'].name = "level2"
        levels['level2'].zoom().helpText = "Nothing can connect to Synapses.\n\
You need to make a connection through the\nnodes to complete the level!"
        levels['level2'].initialize()




        
#Level Four
        levels['level3'] = Level(self.width,self.height,game,[0,0])
        levels['level3'].createConcept((self.width/2,self.height/2))
        levels['level3'].createAssociation(0,(self.width/2,self.height/2))
        levels['level3'].createNode(Synapse,[0,0],(50,self.width/2-300),1)
        levels['level3'].createNode(Node,[0,0],(self.width/2,self.width/2),1,
                               colors["A"])

        levels['level3'].createNode(Node,[0,0],(2*self.width/3,self.width/3),0,
                               colors["C"])
        levels['level3'].createNode(Node,[0,0],(self.width/2,self.height/2+200),1,
                               colors["B"])
        levels['level3'].createNode(Synapse,[0,0],(self.width-50,self.width/2),2)
        levels['level3'].nextLevel = "level4"
        levels['level3'].name = "level3"
        levels['level3'].zoom().helpText = "Don't leave any dead ends, or the\
\nassociation won't be made!"
        levels['level3'].initialize()


#Level Four Test Code
        levels['level4'] = Level(self.width,self.height,game,[0,0])
        levels['level4'].createConcept((self.width/2,self.height/2))
        levels['level4'].createAssociation(0,(self.width/2,self.height/2))
        levels['level4'].createNode(Synapse,[0,0],(50,self.width/2),1)
        levels['level4'].createNode(Node,[0,0],(self.width/2,self.width/2),
                               1,colors["A"])
        levels['level4'].createNode(Node,[0,0],(self.width/2,self.height/2+200),
                                    0,colors["B"])
        levels['level4'].createNode(Node,[0,0],(self.width/2,self.height/3),0,
                               colors["A"])
        
        
        
        levels['level4'].createNode(Synapse,[0,0],(self.width-50,self.width/2),2)
        levels['level4'].nextLevel = "camera_cutscene"
        levels['level4'].name = "level4"
        levels['level4'].zoom().helpText = "Nodes of the same type can't \
connect\nto each other, so watch out!"
        levels['level4'].initialize()
        

#Level Five
        levels['level5'] = Level(self.width,self.height,game,[0])
        levels['level5'].createConcept((self.width/3,self.height/3))
        levels['level5'].zoom([0]).helpText = "Right click to zoom in on a \
puzzle!\nWhen the smaller puzzles are complete,\nuse the dark red dots to \
connect them!"
        #Association 1
        levels['level5'].createAssociation(0,(0,self.height/2))
        levels['level5'].createNode(Synapse,[0,0],(200,self.height/2-100),1)
        levels['level5'].createNode(Synapse,[0,0],(self.width/2,
                                                   self.height/2+100),2)
        levels['level5'].createNode(Synapse,[0,0],(self.width-200,
                                                   self.height/2-100),1)        
        levels['level5'].createNode(Node,[0,0],
                                    (300,self.height/2),1,colors["B"])
        levels['level5'].createNode(Node,[0,0],
                                    (400,self.height/2-200),0,colors["C"])
        levels['level5'].createNode(Node,[0,0],
                                    (500,self.height/2+100),1,colors["A"])
        levels['level5'].zoom([0,0]).helpText = "When you're done, press up to\
 zoom out!"

        #Association 2
        levels['level5'].createAssociation(0,(self.width/2,self.height/3))
        levels['level5'].createNode(Synapse,[0,1],(50,self.width/2-300),1)
        levels['level5'].createNode(Node,[0,1],(self.width/2,self.width/2),1,
                               colors["A"])

        levels['level5'].createNode(Node,[0,1],(2*self.width/3,self.width/3),0,
                               colors["C"])
        levels['level5'].createNode(Node,[0,1],(self.width/2,self.height/2+200),1,
                               colors["B"])
        levels['level5'].createNode(Synapse,[0,1],(self.width-50,self.width/2),2)
        levels['level5'].zoom([0,1]).helpText = "Look familiar?\nPress up to \
zoom out!"
        #Music by Jim Guthrie
        levels['level5'].music = "16 Cabin Music (Bonus Track).mp3"
        levels['level5'].nextLevel = "level6"
        levels['level5'].name = "level5"
        levels['level5'].initialize()



#Level Six

        levels['level6'] = Level(self.width,self.height,game,[0])
        levels['level6'].createConcept((self.width/2,self.height/2))
        #Association 1
        levels['level6'].createAssociation(0,(self.width/3,self.height/3))
        levels['level6'].createNode(Synapse,[0,0],(self.width/2,100),1)
        levels['level6'].createNode(Node,[0,0],(self.width/2-50,150),1,
                                    colors["A"])
        levels['level6'].createNode(Node,[0,0],(self.width/2+100,150),1,
                                    colors["B"])
        levels['level6'].createNode(Node,[0,0],(self.width/2,200),0,
                                    colors["A"])
        levels['level6'].createNode(Synapse,[0,0],(self.width/2,300),1)
        #Association 2
        levels['level6'].createAssociation(0,(self.width/2,self.height/2))
        levels['level6'].createNode(Synapse,[0,1],(self.width/2,100),1)
        levels['level6'].createNode(Node,[0,1],(self.width/2+50,150),1,
                                    colors["A"])
        levels['level6'].createNode(Node,[0,1],(self.width/2,250),1,
                                    colors["B"])
        levels['level6'].createNode(Node,[0,1],(self.width/2+50,300),0,
                                    colors["C"])
        levels['level6'].createNode(Synapse,[0,1],(self.width/2,400),1)
        #Association 3
        levels['level6'].createAssociation(0,(self.width/3,2*self.height/3))
        levels['level6'].createNode(Synapse,[0,2],(self.width/4,self.height/2),1)
        levels['level6'].createNode(Node,[0,2],(self.width/3,self.height/2),1,
                                    colors["A"])
        levels['level6'].createNode(Node,[0,2],(self.width/2,self.height/2),1,
                                    colors["B"])
        levels['level6'].createNode(Node,[0,2],(2*self.width/3,self.height/2),0,
                                    colors["C"])
        levels['level6'].createNode(Synapse,[0,2],(3*self.width/4,300),1)
        levels['level6'].nextLevel = "level7"
        levels['level6'].name = "level6"
        levels['level6'].zoom().helpText = "Only circle connectors with node types\nin common can be linked."
        levels['level6'].initialize()



#Level Seven

        levels['level7'] = Level(self.width,self.height,game,[])
        #concept from last level
        levels['level7'].createConcept((2*self.width/3,self.height/2))
        #Association 1
        levels['level7'].createAssociation(0,(self.width/3,self.height/3))
        levels['level7'].createNode(Synapse,[0,0],(self.width/2,100),1)
        levels['level7'].createNode(Node,[0,0],(self.width/2-50,150),1,
                                    colors["A"])
        levels['level7'].createNode(Node,[0,0],(self.width/2+100,150),1,
                                    colors["B"])
        levels['level7'].createNode(Node,[0,0],(self.width/2,200),0,
                                    colors["A"])
        levels['level7'].createNode(Synapse,[0,0],(self.width/2,300),1)
        #Association 2
        levels['level7'].createAssociation(0,(self.width/2,self.height/2))
        levels['level7'].createNode(Synapse,[0,1],(self.width/2,100),1)
        levels['level7'].createNode(Node,[0,1],(self.width/2+50,150),1,
                                    colors["A"])
        levels['level7'].createNode(Node,[0,1],(self.width/2,250),1,
                                    colors["B"])
        levels['level7'].createNode(Node,[0,1],(self.width/2+50,300),0,
                                    colors["C"])
        levels['level7'].createNode(Synapse,[0,1],(self.width/2,400),1)
        #Association 3
        levels['level7'].createAssociation(0,(self.width/3,2*self.height/3))
        levels['level7'].createNode(Synapse,[0,2],(self.width/4,self.height/2),1)
        levels['level7'].createNode(Node,[0,2],(self.width/3,self.height/2),1,
                                    colors["A"])
        levels['level7'].createNode(Node,[0,2],(self.width/2,self.height/2),1,
                                    colors["B"])
        levels['level7'].createNode(Node,[0,2],(2*self.width/3,self.height/2),0,
                                    colors["C"])
        levels['level7'].createNode(Synapse,[0,2],(3*self.width/4,300),1)
        levels['level7'].nextLevel = "level7"
        levels['level7'].name = "level6"
        

        #concept 2
        levels['level7'].createConcept((self.width/3,self.height/2))
        #Association 1
        levels['level7'].createAssociation(1,(2*self.width/3,self.height/2))
        levels['level7'].createNode(Synapse,[1,0],(self.width/4,self.height/2),
                                    1)
        levels['level7'].createNode(Node,[1,0],(self.width/2,self.height/3),1,
                                    colors["C"])
        levels['level7'].createNode(Node,[1,0],(self.width/2,2*self.height/3),
                                    0,colors["A"])
        levels['level7'].createNode(Node,[1,0],(2*self.width/3,self.height/4),2,
                                    colors["F"])
        levels['level7'].createNode(Synapse,[1,0],(self.width/3,self.height/2),
                                    1)
        #Association 2
        levels['level7'].createAssociation(1,(self.width/4,2*self.height/3))
        levels['level7'].createNode(Synapse,[1,1],(self.width/4,self.height/2),
                                    1)
        levels['level7'].createNode(Node,[1,1],(self.width/2,self.height/3),1,
                                    colors["C"])
        levels['level7'].createNode(Node,[1,1],(2*self.width/3,self.height/4),2,
                                    colors["A"])
        levels['level7'].createNode(Node,[1,1],(self.width/2,2*self.height/3),0,
                                    colors["F"])
        levels['level7'].createNode(Synapse,[1,1],(self.width/3,self.height/2),1)
        levels['level7'].nextLevel = "level8"
        levels['level7'].name = "level7"
        levels['level7'].zoom().helpText = "These 'concept' circles can only be\
\nconnected by links that are\nsimilar, but not the same. Right click on\n\
one and try it out!"
        levels['level7'].initialize()

        
        self.levels = levels

#Level 8

        levels['level8'] = Level(self.width,self.height,game,[])
        #Concept 1
        levels['level8'].createConcept((self.width/3,self.height/2))
        levels['level8'].concepts[0].levelLinks.append(LevelLink(
            Node(self.width,self.height,game,(0,0),0,colors["A"]),
            Node(self.width,self.height,game,(0,0),0,colors["B"]),
            levels['level8'].concepts[0],0))
        levels['level8'].concepts[0].levelLinks.append(LevelLink(
            Node(self.width,self.height,game,(0,0),0,colors["C"]),
            Node(self.width,self.height,game,(0,0),0,colors["B"]),
            levels['level8'].concepts[0],1))
        
        levels['level8'].concepts[0].locked  = True
        levels['level8'].initialize()

        levels['level8'].name = "level8"
        levels['level8'].nextLevel = "credits1"



################################################################################
        #CUTSCENES
################################################################################




############################
#Structure for a cutscene:

#Add an image, if it has one.
#Add animations (writing texts)

#End on adding music and a next level for order.
############################
        
        levels['opening_sequence1'] = Cutscene(game)
        levels['opening_sequence1'].loadImage("openingCutscene/blank.png")
        levels['opening_sequence1'].animations.append(
            WritingText("Are you ready?", (self.width/5,self.height/5),"Times",
                        30,(255,255,255),2))
        levels['opening_sequence1'].animations.append(
            WritingText("I.....I'm not sure.", (3*self.width/5,4*self.height/5),
                        "Times",30,(255,255,255),2))
        levels['opening_sequence1'].animations.append(
            WritingText("I think it's time to turn it on.", (self.width/5,self.height/5),"Times",
                        30,(255,255,255),2))
        levels['opening_sequence1'].animations.append(
            WritingText("Wait.", (3*self.width/5,4*self.height/5),
                        "Times",30,(255,255,255),2))
        levels['opening_sequence1'].animations.append(
            WritingText("He needs a name first.", (3*self.width/7,4*self.height/5),
                        "Times",30,(255,255,255),2))
        
        levels['opening_sequence1'].nextLevel = "opening_sequence2"

        levels['opening_sequence2'] = Cutscene(game)
        #Music by Koji Kondo
        levels['opening_sequence2'].music = "openingCutsceneMusic.wav"
        levels['opening_sequence2'].loadImage("openingCutscene/Opening pic.png")
        levels['opening_sequence2'].animations.append(
            WritingText("", (3*self.width/5,4*self.height/5),
                        "Times",30,(255,255,255),10))
        
        levels['opening_sequence2'].nextLevel = "opening_sequence3"



        levels['opening_sequence3'] = Cutscene(game)
        levels['opening_sequence3'].loadImage("openingCutscene/Digital cutscene1.png")
        levels['opening_sequence3'].animations.append(
            WritingText("", (3*self.width/5,4*self.height/5),
                        "Times",30,(255,255,255),4))
        levels['opening_sequence3'].animations.append(
            WritingText("A name?", (self.width/5,self.height/7),
                        "Times",30,(0,0,0),2))
        levels['opening_sequence3'].animations.append(
            WritingText("Yeah! You know, a name!", (3*self.width/5,self.height/5),
                        "Times",30,(0,0,0),2))
        levels['opening_sequence3'].animations.append(
            WritingText("Something to call him.", (3*self.width/5,self.height/5),
                        "Times",30,(0,0,0),2))
        
        levels['opening_sequence3'].animations.append(
            WritingText("I was just going to call it...", (self.width/5,self.height/6),
                        "Times",30,(0,0,0),1))
        
        levels['opening_sequence3'].animations.append(
            WritingText("The AI. Or something.", (self.width/5,self.height/7),
                        "Times",30,(0,0,0),2))
        
        levels['opening_sequence3'].animations.append(
            WritingText("That's no fun.", (3*self.width/5,self.height/5),
                        "Times",30,(0,0,0),2))

        
        levels['opening_sequence3'].animations.append(
            WritingText("Let's see...", (3*self.width/5,self.height/5),
                        "Times",30,(0,0,0),2))

        
        levels['opening_sequence3'].animations.append(
            WritingText("AI kind of looks like Al!", (3*self.width/5,self.height/5),
                        "Times",30,(0,0,0),1))

        
        levels['opening_sequence3'].animations.append(
            WritingText("I think I'll call him Albert.", (3*self.width/7,self.height/5),
                        "Times",30,(0,0,0),2))
        
        levels['opening_sequence3'].animations.append(
            WritingText("Call it whatever you want.", (self.width/5,self.height/6),
                        "Times",30,(0,0,0),1))

        levels['opening_sequence3'].animations.append(
            WritingText("I'm turning it on.", (self.width/5,self.height/7),
                        "Times",30,(0,0,0),1))
        
        

        levels['opening_sequence3'].nextLevel = "level1"


        #Middle Cutscene
        levels['camera_cutscene'] = Cutscene(game)


        levels['camera_cutscene'].animations.append(
            WritingText("Hey Albert!", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].animations.append(
            WritingText("I got you a present", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].animations.append(
            WritingText("It's a shiny new pair of eyes!",
                        (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].animations.append(
            WritingText("Well, a shiny new camera.", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].animations.append(
            WritingText("But you get the picture.", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].animations.append(
            WritingText("", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),2))
        levels['camera_cutscene'].animations.append(
            WritingText("Anyway, let me hook it up for you.", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['camera_cutscene'].music  = "beep.wav"
        levels['camera_cutscene'].nextLevel = "camera_cutscene2"


        levels['camera_cutscene2'] = Cutscene(game,game.background2)
        levels['camera_cutscene2'].loadImage("drawing.png")
        
        levels['camera_cutscene2'].animations.append(
            WritingText("There you go!", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        
        levels['camera_cutscene2'].animations.append(
            WritingText("How do I look?", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),2))
        levels['camera_cutscene2'].nextLevel = "level5"



        #Credits Cutscene

        
        levels['credits1']  = Cutscene(game)
        levels['credits1'].loadImage("openingCutscene/blank.png")
        #Music by Koji Kondo
        levels['credits1'].music = "openingCutsceneMusic.wav"
        levels['credits1'].animations.append(
            WritingText("", (self.width/5,self.height/7),
                        "Times",30,(0,255,0),1))
        levels['credits1'].animations.append(
            WritingText("./Albert", (self.width/5,self.height/2-60),
                        "Courier",60,(0,255,0),2))
        levels['credits1'].animations.append(
            WritingText("Game by Jonathan Merrin",
                        (self.width/5,self.height/2),
                        "Courier",40,(0,255,0),3))

        levels['credits1'].animations.append(
            WritingText("Story by Jonathan Merrin",
                        (self.width/5,self.height/2),
                        "Courier",40,(0,255,0),3))

        levels['credits1'].animations.append(
            WritingText("Music by:",
                        (self.width/5,self.height/2),
                        "Courier",40,(0,255,0),1))
        levels['credits1'].animations.append(
            WritingText("Kan R. Gao",
                        (self.width/5,self.height/2),
                        "Courier",40,(0,255,0),3))
        levels['credits1'].animations.append(
            WritingText("Jim Guthrie",
                        (self.width/5,self.height/2),
                        "Courier",40,(0,255,0),3))
        levels['credits1'].animations.append(
            WritingText("Beep by Kan R. Gao",
                        (self.width/10,self.height/2),
                        "Courier",40,(0,255,0),3))
        
        levels['credits1'].nextLevel = "credits2"
        




        
        levels['credits2']  = Cutscene(game)
        levels['credits2'].loadImage("digital credits pic.png")
        levels['credits2'].animations.append(
            WritingText("", (self.width/5,self.height/7),
                        "Courier",30,(0,0,0),1))
        levels['credits2'].animations.append(
            WritingText("Crude trackpad drawings by Jonathan Merrin",
                        (10,self.height/7),
                        "Courier",27,(0,0,0),1))
        
        levels['credits2'].animations.append(
            WritingText("Puzzles by Jonathan Merrin",
                        (self.width/5,self.height/7),
                        "Courier",27,(0,0,0),1))

        
        levels['credits2'].animations.append(
            WritingText("Game played by you", (self.width/5,8*self.height/9),
                        "Courier",27,(0,0,0),1))
        levels['credits2'].nextLevel = "splashpage"




        


        #lets you go back to the main menu after the last cutscene
        levels['splashpage'] = game.SplashScreen



    def import_levels(self):
        #sends the levels to the game.
        return self.levels
    
