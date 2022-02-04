##########SET UP THE BOARD###############
init offset = -1
init python:
    def gridAZ(game, x):
        return game.grid[ ord(x[0])-65 ][int(x[1])]

    def isThereAcadaver(case):
        for teen in game.teens:
            if teen.isAlive == 0:
                if teen.x == case.x and teen.y == case.y:
                    return True
        return False

    def distBetween(start, destination, search_size, iftile, ifwall, ifdoor, ifteen, ifdoom):
        class Cell:
            def __init__(self,start,destination,gcost, state = "???", parent=""):
                self.x = start.x
                self.y = start.y
                self.gcost = gcost
                self.hcost = abs(start.x - destination.x) + abs(start.y - destination.y)
                self.fcost = self.gcost + self.hcost
                self.state = state
                self.parent = parent
            def __repr__(self):
                return " x" +str(self.x)+ ":y" +str(self.y)+" "

        def trouve_enfant(x, array):
            if x != "":
                array.append(x)
                trouve_enfant(x.parent, array)
            return array
        cells = {}
        cells[start.x,start.y] = Cell(start,destination,0, "open")

        array = {}
        for key, value in cells.iteritems():
            if cells[key].state == "open":
                array[key] = cells[key]

        for irfrrr in range(search_size):
            array = {}
            for key, value in cells.iteritems():
                if cells[key].state == "open":
                    array[key] = cells[key]

            min = 99
            currentArray = []
            for key, value in array.iteritems():
                if array[key].fcost < min:
                    currentArray = [ array[key] ]
                    min = array[key].fcost
                if array[key].fcost == min:
                    currentArray.append( array[key] )

            min = 99
            for k in currentArray:
                if k.hcost < min:
                    current = k

            current.state = "closed"

            if (current.x,current.y) == (destination.x, destination.y):
                array = []
                array = trouve_enfant(current.parent, array)

                if len(array)>0:
                    array.insert(0, destination )
                    del array[-1]

                return [current.fcost, list(reversed(array))]

            for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                pos = {}
                pos.x = current.x + direction[0]
                pos.y = current.y + direction[1]

                if not (pos.x,pos.y) in cells:
                    neighbor = Cell( pos, destination, current.gcost+1, "???",current)
                else:
                    neighbor = Cell( pos, destination, current.gcost+1, cells[pos.x,pos.y].state,current) #is current the dad?


                if (not game.isCrossable( x2=neighbor.x, y2=neighbor.y, x=current.x, y=current.y, iftile=iftile, ifdoom = ifdoom, ifwall=ifwall, ifdoor=ifdoor, ifteen=ifteen ) ) or neighbor.state == "closed":
                    pass

                else:
                    if neighbor.state != "open" or neighbor.fcost < cells[neighbor.x,neighbor.y].fcost:
                        cells[pos.x,pos.y] = neighbor
                        if neighbor.state != "open":
                            cells[pos.x,pos.y] = neighbor
                            cells[pos.x,pos.y].state = "open"

        return [999,""]

    class Character:
        # init method or constructor
        def __init__(self, name, x, y):
            self.name = name
            self.x = x
            self.y = y
            self.img = {}
            self.AP = 1 #How much AP does it have?
            self.prex = 0
            self.prey = 0

            self.img.idle = name + "-idle.png"
            self.img.hover = name + "-hover.png"
            self.img.premove = name + "-premove.png"
            self.img.noAP = name + "-noAP.png"
            self.img.dead = name + "-dead.png"

            self.stat = {}
            self.stat.vis = 10
            self.stat.move = 4

            self.isAlive = 1
            self.inventory = {}

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
            # self.removeAP(1)
            game.actions = []
            game.state = "action"
            # if game.grid[self.y][self.x].itemType != None:
            #     if game.interaction(itemType , 0):
            #         game.actions.append( game.interaction(itemType , 0) )
            for case in game.inrange(self.x, self.y, 1):
                if case.itemType != None:
                    if case.interaction(case.itemType , 1, self, case):
                        game.actions.append( case.interaction(case.itemType , 1, self, case) ) # { nom:nom, function:function}

            if isThereAcadaver(case):
                game.actions.append( { "text": "take items", "label": "lab_takeitems", "variables":[self,case] } )

            try:
                settings["actions"][_09toAZ(self.x, self.y)]
            except:
                pass
            else:
                game.actions.append( settings["actions"][_09toAZ(self.x, self.y)] ) #str(ord(y)-65

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
        # def move(self):
        #     renpy.call("lab_doommove", self)

        def sound_walk(self,case):
            if game.grid[case.y][case.x].type==200:
                renpy.music.play("audio/step-water-2.wav", channel='sound')
            elif isThereAcadaver(case):
                renpy.music.play("audio/step-water-1.wav", channel='sound')
            else:
                renpy.music.play("audio/step4.wav", channel='sound')
            renpy.pause(0.5)

        def move(self):
################################################################################
#######DECISION MAKING: first try if there's anyone near reacheable, then just randomwalk otherwise

            for doom in game.dooms:
                target = [99,""]
                cible = ""

                #####  SEARCH ONLY PATHS WITH DOORS OPEN  #######
                for teen in game.teens:
                    if teen.isAlive:
                        distance = distBetween(start=doom, destination=teen, search_size=15, ifteen=False, iftile=True, ifdoom=False,ifwall=True,ifdoor=(not doom.canOpenDoors))
                        print("OPENED DOORS: cible:"+teen.name+" distance:" + str(distance[0]))
                        if target[0] > distance[0]:
                            target = distance
                            cible = teen

                if target[0] == 99: 
                    #####  SEARCH EVERYWHERE FOR THE CLOSEST UP TO 20   #######
                    for teen in game.teens:
                        if teen.isAlive:
                            distance = distBetween(start=doom, destination=teen, search_size=30, ifteen=False, iftile=True, ifdoom=False,ifwall=True,ifdoor=(not doom.canOpenDoors))
                            print("CLOSED cible:"+teen.name+" distance:" + str(distance[0]))
                            if target[0] > distance[0]:
                                target = distance
                                cible = teen

                print("target:"+str(target[1]))
                if target[0] == 99: ##HERE ITS THE SAME AS RANDOMWALK
                    renpy.call("lab_doommove_random", doom)
                else:
                    renpy.call("lab_doommove_track", doom, cible, target)
            renpy.jump(lab_turnChange)