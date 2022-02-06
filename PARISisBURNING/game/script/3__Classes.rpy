##########SET UP THE BOARD###############
init offset = -1
init python:

    class Character:
        # init method or constructor
        def __init__(self, game, name, x, y):
            self.name = name
            self.x = x
            self.y = y
            self.img = {}
            self.AP = 1 #How much AP does it have?
            self.prex = 0
            self.prey = 0

            game.grid[y][x].occupied = "teen"

            self.img.idle = name + "-idle.png"
            self.img.hover = name + "-hover.png"
            self.img.premove = name + "-premove.png"
            self.img.noAP = name + "-noAP.png"
            self.img.dead = name + "-dead.png"

            self.stat = {}
            self.stat.vis = 10
            self.stat.move = 4

            self.isAlive = 1
            self.inventory = []

        def __repr__(self):
            return self.name

        def sprite(self):
            if self.isAlive:
                if game.state == "moving" and game.premoving_who == self:
                    return self.img.premove
                else:
                    if self.AP > 0:
                        return self.img.idle
                    else:
                        return self.img.noAP
            else:
                return self.img.dead

        def premove(self):
            if game.state == "waiting" and self.AP > 0:
                game.state = "moving"
                game.premoving_who = self
                game.premoving_where = game.inrange2(x=self.x, y=self.y, howfar=self.stat.move, ifteen=False)

        def move(self, cell):
            if cell.occupied == 0 or (cell.x==self.x and cell.y==self.y):
                game.grid[self.y][self.x].occupied = 0
                self.prex = self.x
                self.prey = self.y

                self.x = cell.x
                self.y = cell.y
                game.grid[self.y][self.x].occupied = "teen"
                # game.updateVision()
                game.premoving_where = ""
                self.action()

                if game.totalAP() <= 0:
                    renpy.jump( "lab_turnChange" )
                else:
                    renpy.jump( "lab_gameloop" )

        def action(self):

            game.actions = []
            game.state = "action"
            
            case = game.grid[self.y][self.x]

            if game.isThereAcadaver(case):
                game.actions.append( { "text": "Scarvenge", "label": "lab_takeitems", "variables":[self,case]} )

            print(self.y,self.x)
            for action in game.grid[self.y][self.x].onAction:
                action.add_action(game, self, game.grid[self.y][self.x], 0)

            
            for case in game.inrange(self.x, self.y, 1):
                for action in case.onAction:
                    action.add_action(game, self, case, 1)

            ####add items:
            for item in self.inventory:
                item.add_action(game, self)

            obj = { "text": "PASS", "label": "lab_passTurn", "variables":self }
            game.actions.append( obj )

        def cancelMov(self):
            game.grid[self.y][self.x].occupied = 0
            self.removeAP(-1)
            self.x = self.prex
            self.y = self.prey
            game.grid[self.y][self.x].occupied = 1
            game.state = "moving"
            game.premoving_who = self
            game.premoving_where = game.inrange2(x=self.x, y=self.y, howfar=self.stat.move, ifteen=False)

        def endAction(self):
            game.premoving_who = ""
            game.state = "waiting"
            game.grid[self.y][self.x].onEvent(game)

            # if len(self.actions) == 1:
            #     self.passTurn()

            if game.totalAP() <= 0:
                renpy.jump( "lab_turnChange" )

        def passTurn(self):
            game.state = "waiting"
            if game.totalAP() <= 0:
                renpy.jump( "lab_turnChange" )

        def removeAP(self, x):
            self.AP -= x
            if game.totalAP() <= 0:
                renpy.jump( "lab_turnChange" )

        def die(self):
            if self.isAlive == 1:
                self.isAlive = 0
                game.grid[self.y][self.x].occupied = 0
                if self.name in ["william","darryl"]: #is that a boi
                    renpy.music.play("audio/manstab.ogg", channel='sound')
                else:
                    renpy.music.play("audio/girlstab.ogg", channel='sound')
                renpy.pause(0.5)

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
        def __init__(self, name, x, y, idle = "doom-idle.png", hover = "doom-idle.png", premove = "doom-idle.png", canOpenDoors = False):
            self.name = name
            self.x = x
            self.y = y

            self.stat = {}
            self.stat.move = 3

            self.img = {}
            self.img.idle = idle
            self.img.hover = hover
            self.img.premove = premove
            self.img.invisible = "doom-invisible.png"

            self.canOpenDoors = canOpenDoors
        def __repr__(self):
            return self.name

        def sprite(self):
            if game.grid[self.y][self.x].visibility == 1 or game.debug_mode:
                return self.img.idle
            else:
                return self.img.invisible

        def sound_walk(self,case):
            if game.grid[case.y][case.x].type==200:
                renpy.music.play("audio/step-water-2.wav", channel='sound')
            elif game.isThereAcadaver(case):
                renpy.music.play("audio/step-water-1.wav", channel='sound')
            else:
                renpy.music.play("audio/step4.wav", channel='sound')
            renpy.pause(0.5)

        def move(self):

#######DECISION MAKING: first try if there's anyone near reacheable, then just randomwalk otherwise

            target = [99,""]
            cible = ""

            #####  SEARCH PATHS WITH OPENABLE DOORS  #######
            for teen in game.teens:
                if teen.isAlive:
                    distance = distBetween(start=self, destination=teen, search_size=self.stat.move*20, ifteen=False, ifdoom=False, canOpenDoors=self.canOpenDoors)
                    print("cible:"+teen.name+" distance:" + str(distance[0]))
                    if target[0] > distance[0]:
                        target = distance
                        cible = teen

            print("target:"+str(target[1]))
            if target[0] == 99: ##HERE ITS THE SAME AS RANDOMWALK
                self.move_random()
            else:
                self.move_track(cible, target)

            for teen in game.teens:
                if self.x == teen.x and self.y == teen.y:
                    teen.die()


        def move_random(self):
            for i in range(self.stat.move):
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
                        i = self.stat.move #end the for loop
                    else:
                        randomInd += 1
                        randomDir = direction[ randomInd%4 ]

                self.x = self.x + randomDir[0]
                self.y = self.y + randomDir[1]

                self.sound_walk(self)

                game.grid[self.y][self.x].occupied = "doom"
                for teen in game.teens:
                    if self.x == teen.x and self.y == teen.y:
                        game.debug = "172"
                        renpy.call("lab_kill",teen)


        def move_track(self,cible,target):
            for i in range( self.stat.move ):

                if len(target[1]) > i:

                    #can he just straight up walk there?
                    if game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=self.x, y=self.y, ifdoom = False, ifwall=True, ifdoor=True, ifteen=False, lastMovement=(len(target[1]) == 0) ):

                        game.grid[self.y][self.x].occupied = 0
                        self.x = target[1][i].x
                        self.y = target[1][i].y
                        self.sound_walk(self)

                    #or is there a door?
                    elif self.canOpenDoors and game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=self.x, y=self.y,
                        ifdoom = False, ifwall=True, ifdoor=False, ifteen=False, lastMovement=(len(target[1]) == 0) ):

                            print("theres a door")

                            if action_door(self.x,self.y, target[1][i].x,target[1][i].y):
                                game.grid[self.y][self.x].occupied = 0
                                self.x = target[1][i].x
                                self.y = target[1][i].y
                                self.sound_walk(self)
                            else:
                                i = self.stat.move

                    else:
                        i = self.stat.move

                game.grid[self.y][self.x].occupied = "doom"
            