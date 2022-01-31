##########SET UP THE BOARD###############
init offset = -1
init python:
    def gridAZ(game, x):
        return game.grid[ ord(x[0])-65 ][int(x[1])]

    def id2pos(x):
        return int(x * settings["tilesize"])

    def pos2id(x):
        return int(x / settings["tilesize"])

    def isThereAcadaver(case):
        for teen in game.teens:
            if teen.isAlive == 0:
                if teen.x == case.x and teen.y == case.y:
                    return True
        return False

    def sound_walk(case):
        if game.grid[case.y][case.x].type==200:
            renpy.music.play("audio/step-water-2.wav", channel='sound')
        elif isThereAcadaver(case):
            renpy.music.play("audio/step-water-1.wav", channel='sound')
        else:
            renpy.music.play("audio/step4.wav", channel='sound')
        renpy.pause(0.5)
    # def getMousePos():
    #     x, y = pygame.mouse.get_pos()
    #     store.mousex = x
    #     store.mousey = y
    #     print(x,y)

    # def getMouseId():
    #     x, y = pygame.mouse.get_pos()
    #     store.mousexid = pos2id(x)
    #     store.mouseyid = pos2id(y)
    #     print(x,y)

    def distBetween(start, destination, game, search_size, collisionWall = True, collisionDoor=True):
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

        #while len(array)>0:
        for irfrrr in range(search_size):
            array = {}
            for key, value in cells.iteritems():
                if cells[key].state == "open":
                    array[key] = cells[key]

            # print("array")
            # print(array)

            min = 99
            currentArray = []
            for key, value in array.iteritems():
                if array[key].fcost < min:
                    currentArray = [ array[key] ]
                    min = array[key].fcost
                if array[key].fcost == min:
                    currentArray.append( array[key] )

            # print("currentArray")
            # print(currentArray)

            min = 99
            for k in currentArray:
                if k.hcost < min:
                    current = k

            # print(k)
            current.state = "closed"

            if (current.x,current.y) == (destination.x, destination.y):
                array = []
                array = trouve_enfant(current.parent, array)

                if len(array)>0:
                    array.insert(0, destination )
                    del array[-1]
                    print array

                return [current.fcost, array]

            for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                pos = {}
                pos.x = current.x + direction[0]
                pos.y = current.y + direction[1]

                if not (pos.x,pos.y) in cells:
                    # cells[pos.x,pos.y] = Cell(pos,destination,current.gcost+1,"open",current.parent)
                    neighbor = Cell( pos, destination, current.gcost+1, "???",current)
                else:
                    neighbor = Cell( pos, destination, current.gcost+1, cells[pos.x,pos.y].state,current) #is current the dad?

                if collisionWall:
                    if (not game.isCrossable(neighbor.x,neighbor.y,current.x,current.y) ) or neighbor.state == "closed":
                        pass
                    else:
                        if neighbor.state != "open" or neighbor.fcost < cells[neighbor.x,neighbor.y].fcost:
                            cells[pos.x,pos.y] = neighbor
                            if neighbor.state != "open":
                                cells[pos.x,pos.y] = neighbor
                                cells[pos.x,pos.y].state = "open"
                else:
                    if neighbor.state == "closed":
                        pass
                    else:
                        if neighbor.state != "open" or neighbor.fcost < cells[neighbor.x,neighbor.y].fcost:
                            cells[pos.x,pos.y] = neighbor
                            if neighbor.state != "open":
                                cells[pos.x,pos.y] = neighbor
                                cells[pos.x,pos.y].state = "open"

        print("lol cant reach??")
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
                game.premoving_where = game.inrange2(self.x, self.y, self.stat.move, False)

        def move(self, cell):
            if cell.occupied == 0 or (cell.x==self.x and cell.y==self.y):
                game.grid[self.y][self.x].occupied = 0
                self.prex = self.x
                self.prey = self.y

                self.x = cell.x
                self.y = cell.y
                game.grid[self.y][self.x].occupied = 1
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

            x = self.x
            y = self.y
            print( chr(ord('@')+y+1) + str(x) )
            try:
                settings["actions"][ chr(ord('@')+y+1) + str(x) ]
            except:
                pass
            else:
                game.actions.append( settings["actions"][ chr(ord('@')+y+1) + str(x) ] ) #str(ord(y)-65

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
            game.premoving_where = game.inrange2(self.x, self.y, self.stat.move, False)

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

    class Slasher:
        # init method or constructor
        def __init__(self, name, x, y, idle = "doom-idle.png", hover = "doom-idle.png", premove = "doom-idle.png"):
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
        def __repr__(self):
            return self.name
        # def hover(self):
        #     if game.grid[self.y][self.x].visibility == 1:
        #         return self.img.hover
        #     else:
        #         return self.img.invisible
        #display which sprite
        def sprite(self):
            if game.grid[self.y][self.x].visibility == 1:
                return self.img.idle
            else:
                return self.img.invisible
        def move(self):
            renpy.call("lab_doommove_track", self)
