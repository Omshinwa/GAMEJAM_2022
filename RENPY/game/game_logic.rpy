##########SET UP THE BOARD###############

init python:

    import math
    import random

    settings = {}
    settings["tilesize"] = 96.0 #in pixel
    settings["resolution"] = (1920.0,1080.0)

    def id2pos(x):
        return int(x * settings["tilesize"])

    def pos2id(x):
        return int(x / settings["tilesize"])

    class Square:
        def __init__(self, x, y, isStand = 0, visibility = 0):
            self.x = x
            self.y = y
            self.xpos = x * settings["tilesize"]
            self.ypos = y * settings["tilesize"]
            self.isStand = isStand #can we stand on it or not?
            self.visibility = visibility
            self.img = {}
            self.img.idle = "game-UI/cell-idle.png"
            self.img.hover = "img_cell_hover"
            self.img.unstand = "game-UI/cell-unstand.png"
            self.empty = 1 - self.isStand #0 theres nothing there

        def __repr__(self):
            return " (x" +str(self.x)+ ":y" +str(self.y)+") "
        def sprite(self):
            if self.isStand == 1:
                img = self.img.idle
            else:
                img = self.img.unstand
            return img


    class Character:
        # init method or constructor
        def __init__(self, name, x, y,
        idle = "teen-idle.png",
        hover = "teen-hover.png",
        premove = "teen-premove.png",
        noAP = "teen-noAP.png"):
            self.name = name
            self.x = x
            self.y = y
            self.img = {}
            self.AP = 1 #How much AP does it have?
            self.img.idle = idle
            self.img.hover = hover
            self.img.premove = premove
            self.img.noAP = noAP

        def __repr__(self):
            return self.name

        def sprite(self):
            if game.state == "waiting":
                if self.AP > 0:
                    return self.img.idle
                else:
                    return self.img.noAP
            if game.state == "moving" and game.premoving_who == self:
                return self.img.premove

        def premove(self):
            if game.state == "waiting" and self.AP > 0:
                game.state = "moving"
                game.premoving_who = self

        def move(self, cell):
            if cell.empty == 0:
                game.grid[self.y][self.x].empty = 0
                self.x = cell.x
                self.y = cell.y
                game.grid[self.y][self.x].empty = self
                game.state = "waiting"
                self.removeAP(1)
                game.updateVision()
                #some complicated pathfinding

        def removeAP(self, x):
            self.AP -= x
            if game.totalAP() <= 0:
                game.turnChange()


    class Slasher:
        # init method or constructor
        def __init__(self, name, x, y, idle = "doom-idle.png", hover = "doom-idle.png", premove = "doom-idle.png"):
            self.name = name
            self.x = x
            self.y = y
            self.stat = {}
            self.stat.move = 4
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
            game.grid[self.y][self.x].empty = 0

            self.x = self.x + random.randint(-1,1)
            if self.x < 0: self.x = 0
            if self.x > game.maxX: self.x = game.maxX

            self.y = self.y + random.randint(-1,1)
            if self.y < 0: self.y = 0
            if self.y > game.maxX: self.y = game.maxY

            game.grid[self.y][self.x].empty = self

            #some complicated pathfinding

    class Game:

        def __init__(self):
            self.ui = {}
            self.grid = []
            self.gridlist = []
            self.debug_mode = False
            self.teens = []
            pass

        def turnChange(self):
            self.updateVision()
            if self.state == "waiting":
                self.state = "doom"
                for doom in game.dooms:
                    doom.move()
                    self.turnChange()

            elif self.state == "doom":
                self.state = "waiting"
                self.restore_totalAP()

        def restore_totalAP(self):
            for teen in self.teens:
                teen.AP = 1

        def totalAP(self):
            totalAP = 0
            for teen in self.teens:
                totalAP += teen.AP
            return totalAP

        def inrange(self, x, y, howfar):
            #very naive way of giving back an array of every square in howfar range
            array=[]
            for xi in range(-howfar ,howfar+1):
                range2 = abs(abs(xi)-howfar)
                for yi in range(-range2, range2+1):
                    if yi + y>=0 and xi + x>=0:
                        try:
                            game.grid[yi + y][xi + x]
                        except:
                            pass
                        else:
                            array.append(game.grid[yi + y][xi+ x])
            return array

        def updateVision(self):
            for case in game.gridlist:
                case.visibility = 0
            for teen in game.teens:
                for case in self.inrange( teen.x , teen.y , 3):
                    case.visibility = 1


    game = Game()
    game.maxY =  math.ceil(settings["resolution"][1]/settings["tilesize"])
    game.maxX = math.ceil(settings["resolution"][0]/settings["tilesize"])
    for y in range( game.maxY ):
        game.grid.append([]) #add first row
        for x in range( game.maxX ):
            if y==0 or x==0 or x==math.ceil(settings["resolution"][0]/settings["tilesize"])-1 or y==math.ceil(settings["resolution"][1]/settings["tilesize"])-1:
                game.grid[y].append( Square(x=x, y=y, isStand = 0) )
            else:
                game.grid[y].append( Square(x=x, y=y, isStand = 1) )
            game.gridlist.append( game.grid[y][x] )

    game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30


    game.teens.append( Character( name = "Adam", x = 3, y = 3) )
    game.state = "waiting"
    game.dooms = []
    game.dooms.append( Slasher(name="Slasher", x=6, y=6) )
