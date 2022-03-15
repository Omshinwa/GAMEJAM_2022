##########SET UP THE BOARD###############
init offset = -1
init python:

    class Character:
        # init method or constructor
        def __init__(self, game, x, y, items, file, name=None, stat={"vision":10, "move":4} ):

            if name is None:
                self.name = file.capitalize()
            else:
                self.name = name

            if items == None:
                self.inventory = []
            else:
                self.inventory = [items]
            
            self.file = file
            self.x = x
            self.y = y
            self.img = {}
            self.AP = 2 #How much AP does it have?
            self.prex = 0
            self.prey = 0
            self.maxAP = 2
            self.movePerTurn = 1

            if file in  ["william","gwenael","morgan","franky","darryl","kayleigh"]:
                self.sex = "male"
            else:
                self.sex = "female"

            self.stat = stat

            if not "isStrong" in self.stat:
                self.stat["isStrong"] = False
            if not "isBlind" in self.stat:
                self.stat["isBlind"] = False
            if self.stat["isBlind"]:
                self.stat["vision"] = 0

            self.isAlive = 1

            game.grid[y][x].occupied = "teen"
            
            self.img.big = self.file + "-big.png"
            self.img.idle = self.file + "-idle.png"
            self.img.hover = self.file + "-hover.png"
            self.img.premove = self.file + "-premove.png"
            self.img.noAP = self.file + "-noAP.png"
            # self.img.dead =  name + "-dead.png"
            

        def __repr__(self):
            return self.name

        def sprite(self):
            if self.isAlive:
                if game.state == "moving" and game.premoving.who == self:
                    return self.img.premove
                else:
                    if self.AP > 0:
                        return self.img.idle
                    else:
                        return self.img.noAP
            else:
                return "game-UI/cell-blank.png" #self.img.dead

        #WAIT STATE = you can move characters/click on things
        #MOVING = you chose a character, you can only interact with him
        #you can CANCEL the move
        #PRE_ACTION = you chose where to put your character, you can choose an action
        #ACTION = sometimes this lead to another option select screen (splash water)

        def premove(self):
            if self.AP > 0:
                game.state = "moving"
                game.premoving.who = self
                game.premoving.where = game.inrange2(x=self.x, y=self.y, howfar=self.stat["move"], exception_arr=["teen"])

        def move(self, cell):
            if cell.occupied == 0:
                self.AP -= 1
                game.grid[self.y][self.x].occupied = 0

                self.x = cell.x
                self.y = cell.y
                self.movePerTurn -= 1
                game.grid[self.y][self.x].occupied = "teen"
                # game.updateVision()
                game.premoving.where = []
                if self.AP > 0:
                    self.action()
                else:
                    game.state = "waiting"

                if game.totalAP() <= 0:
                    renpy.jump( "lab_turnChange" )
                # else:
                #     renpy.jump( "lab_gameloop" )

        def select(self):
            self.prex = self.x
            self.prey = self.y
            self.action()

        def action(self):
            game.premoving.who = self
            game.actions = []
            game.state = "select"
            case = game.grid[self.y][self.x]

            if game.isThereAcadaver(case):
                game.actions.append( { "text": "Scarvenge", "label": "lab_takeitems", "variables":[self,case]} )

            for action in game.grid[self.y][self.x].onAction:
                action.add_action(game, self, game.grid[self.y][self.x], 0)
            
            for case in game.inrange(self.x, self.y, 1):
                if game.isCrossable(x2=case.x, y2=case.y, x=self.x, y=self.y, iftile=False, ifwall=True, ifdoor=True, ifoccupied=False):
                    for action in case.onAction:
                        action.add_action(game, self, case, 1)

            ####add items:
            for item in self.inventory:
                item.add_action(game, self)

            game.actions.append( { "text": "PASS", "label": "lab_passTurn", "variables":self } )
            if self.AP >=1 and self.movePerTurn > 0:
                game.actions.append( { "text": "MOVE", "label": "lab_teen_move", "variables":self } )

            # obj = { "text": "MOVE", "label": "lab_passTurn", "variables":self }
            # game.actions.append( obj )

        def cancelMov(self):

            game.grid[self.y][self.x].occupied = 0
            self.x = self.prex
            self.y = self.prey
            game.grid[self.y][self.x].occupied = "teen"

            if game.state == "action":
                if self.movePerTurn == 0:
                    self.removeAP(-1)
                    self.movePerTurn += 1
                self.select()
            elif game.state == "select":
                if self.movePerTurn == 0:
                    self.removeAP(-1)
                    self.movePerTurn += 1
                    self.premove()
                else:
                    game.state = "waiting"
            else:
                print("WOW THERES AN EXCEPTION 154")

        def removeAP(self, x):
            self.AP -= x
            if game.totalAP() <= 0:
                renpy.jump( "lab_turnChange" )

        def die(self):
            if self.isAlive == 1:
                self.isAlive = 0
                game.grid[self.y][self.x].occupied = 0
                if self.sex == "male": #is that a boi
                    renpy.music.play("audio/manstab.ogg", channel='sound')
                elif self.sex == "female":
                    renpy.music.play("audio/girlstab.ogg", channel='sound')
                game.grid[self.y][self.x].onFire = -2
                renpy.pause(0.5)

        @staticmethod
        def restore_totalAP():
            for teen in game.teens:
                teen.AP = teen.maxAP * teen.isAlive
                teen.movePerTurn = 1

#########################################################################################################################################
#####     #####     #####     #####     #####     #####     #####     #####
#####     #####     #####     #####     #####     #####     #####     #####
#    #####     #####     #####     #####     #####     #####     #####     #####
#    #####     #####     #####     #####     #####     #####     #####     #####
#####     #####     #####     #####     #####     #####     #####     #####
#####     #####     #####     #####     #####     #####     #####     #####
#########################################################################################################################################

    class Slasher:
        # init method or constructor
        def __init__(self, name, x, y, canOpenDoors = False):
            self.name = name
            self.x = x
            self.y = y
            self.stat = {}
            self.stat["move"] = 4

            self.file = name
            self.img = {}
            self.img.idle = name + "-idle.png"
            self.img.big = name + "-big.png"
            # self.img.hover = hover + "-hover.png"
            # self.img.premove = premove + "-premove.png"
            self.img.invisible = "empty.png"

            self.canOpenDoors = canOpenDoors
        def __repr__(self):
            return self.name

        def sprite(self):
            if game.grid[self.y][self.x].visibility == 1 or game.debug_mode:
                return self.img.idle
            else:
                return self.img.invisible

        def sound_walk(self,case):
            if game.isThereAcadaver(case):
                renpy.play("audio/step-body.ogg", channel='sound', relative_volume=self.distant_sound())
            elif game.grid[case.y][case.x].onFire == -1 or game.grid[case.y][case.x].type=="w":
                renpy.play("audio/step-water-1.wav", channel='sound', relative_volume=self.distant_sound())
            else:
                renpy.play("audio/step-normal.ogg", channel='sound', relative_volume=self.distant_sound())
                
            renpy.pause(0.5)

        def distant_sound(self):
            sound_volume = max( 1/2**( self.closest_teen()[1] /4.0), 0.06) # min( 0.75**( (closest_teen_distance-3)/2.0), 1.0)
            return sound_volume

        # params: [teen, distance]
        def closest_teen(self):
            closest_teen_distance = 99
            closest_teen = None
            for teen in game.teens:
                if teen.isAlive:
                    distance = abs(teen.x-self.x)+abs(teen.y-self.y)
                    if distance < closest_teen_distance:
                        closest_teen_distance = distance
                        closest_teen = teen
            return (closest_teen, closest_teen_distance)

#######DECISION MAKING: first try if there's anyone near reacheable, then just randomwalk otherwise
        def move(self):
            target = [999,""]
            cible = ""

            #####  SEARCH PATHS WITH OPENABLE DOORS  #######
            for teen in game.teens:
                if teen.isAlive:
                    distance = distBetween(start=self, destination=teen, search_size=self.stat["move"]*20, exception_arr=["teen"], canOpenDoors=self.canOpenDoors)
                    if distance[0] < target[0]:
                        target = distance
                        cible = teen

            print("cible1:"+str(target[1]) + " distance:" + str(target[0]) )

            if target[0] >= 999: ## GO TO THE CLOSEST THINKING THERE IS NO DOOR

                for teen in game.teens:
                    if teen.isAlive:
                        distance = abs(teen.x-self.x)+abs(teen.y-self.y)
                        if target[0] > distance:
                            target = distBetween(start=self, destination=teen, search_size=self.stat["move"]*50, exception_arr=["teen"], ifdoor=False)
                            cible = teen
                print("cible2:"+teen.name+" distance:" + str(target[0]))


            if target[0] >= 999: ## GO TO THE CLOSEST NAIVELY

                for teen in game.teens:
                    if teen.isAlive:
                        distance = abs(teen.x-self.x)+abs(teen.y-self.y)
                        if target[0] > distance:
                            target = distBetween(start=self, destination=teen, search_size=self.stat["move"]*50, exception_arr=["teen"], ifdoor=False, iftile = False, ifwall=False, ifoccupied=False)
                            cible = teen
                print("cible3:"+teen.name+" distance:" + str(target[0]))
                
            # else:
            self.move_track(cible, target)

            for teen in game.teens:
                if self.x == teen.x and self.y == teen.y:
                    teen.die()


        def move_random(self):
            for i in range(self.stat["move"]):
                game.grid[self.y][self.x].occupied = 0
                validMove = False

                while validMove == False:
                    direction = [(-1,0),(0,1),(1,0),(0,-1)]
                    randomInd = random.randint(0,3)
                    randomDir = direction[ randomInd ]
                    if game.isCrossable(self.x+randomDir[0],self.y+randomDir[1],self.x,self.y):
                        validMove = True
                    elif randomInd >= randomInd%4 + 4:
                        validMove = True
                        randomDir = (0,0)
                        i = self.stat["move"] #end the for loop
                    else:
                        randomInd += 1
                        randomDir = direction[ randomInd%4 ]

                self.x = self.x + randomDir[0]
                self.y = self.y + randomDir[1]

                self.sound_walk(self)

                game.grid[self.y][self.x].occupied = "doom"
                for teen in game.teens:
                    if self.x == teen.x and self.y == teen.y:
                        print("237" + teen.name)
                        teen.die()


        def move_track(self,cible,target):
            for i in range( self.stat["move"] ):

                if len(target[1]) > i:

                    #can he just straight up walk there?
                    if game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=self.x, y=self.y, ifwall=True, ifdoor=True, exception_arr=["teen","doom"], lastMovement=(len(target[1]) - i == 1) ):

                        game.grid[self.y][self.x].occupied = 0
                        self.x = target[1][i].x
                        self.y = target[1][i].y
                        self.sound_walk(self)

                    #or is there a door?
                    elif self.canOpenDoors and game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=self.x, y=self.y,
                        exception_arr=["teen"], ifwall=True, ifdoor=False, lastMovement=(len(target[1]) - i == 1) ):

                            print("theres a door")

                            if self.action_door(self.x,self.y, target[1][i].x,target[1][i].y):
                                game.grid[self.y][self.x].occupied = 0
                                self.x = target[1][i].x
                                self.y = target[1][i].y
                                self.sound_walk(self)
                            else:
                                i = self.stat["move"]

                    else:
                        i = self.stat["move"]

                game.grid[self.y][self.x].occupied = "doom"

        def action_door(self,x,y,x2,y2): #currently used by slashers

            for action in game.grid[y][x].onAction:
                if action.name == "door":
                    vari = action.variables

                    a = game.grid[y][x].occupied or game.grid[y][x].isStand == 0
                    b = game.grid[y2][x2].occupied or game.grid[y2][x2].isStand == 0

                    if a and b:
                        renpy.play("audio/doorfail.ogg", channel='sound', relative_volume= self.distant_sound())
                        return False
                    else:
                        if game.data_line[vari]== 2:
                            renpy.play("audio/opendoor1.mp3", channel='sound', relative_volume= self.distant_sound())
                            renpy.pause(0.5)
                            game.data_line[vari] = 3
                        elif game.data_line[vari]== 3:
                            renpy.play("audio/closedoor1.wav", channel='sound', relative_volume= self.distant_sound())
                            renpy.pause(0.5)
                            game.data_line[vari] = 2
                        return True

            return False
            