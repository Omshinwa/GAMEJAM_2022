##########SET UP THE BOARD###############

init python:

    import math

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
            self.x = cell.x
            print cell.x
            print cell.y
            self.y = cell.y
            game.state = "waiting"
            self.AP -= 1
            #some complicated pathfinding

    class Slasher:
        # init method or constructor
        def __init__(self, name, x, y, idle = "doom-idle.png", hover = "doom-idle.png", premove = "doom-idle.png"):
            self.name = name
            self.x = x
            self.y = y
            self.move = 4
            self.img = {}
            self.img.idle = idle
            self.img.hover = hover
            self.img.premove = premove
            self.img.invisible = "doom-invisible.png"

        def __repr__(self):
            return self.name

        def hover(self):
            if game.grid[self.y][self.x].visibility == 1:
                return self.img.hover
            else:
                return self.img.invisible

        def sprite(self):
            if game.grid[self.y][self.x].visibility == 1:
                return self.img.idle
            else:
                return self.img.invisible

        def move(self, cell):
            self.x = cell.x
            print cell.x
            print cell.y
            self.y = cell.y
            game.state = "waiting"
            #some complicated pathfinding

    class Game:
        def inrange((x,y), range):
            for i in range(-x,x+1):
                pass
            return array
        def updateVision(self):
            for teen in game.teens:
                for case in game.inrange( (teen.x, teen.y), 3):
                    case.visibility = 1

    game = {}
    game.ui = {}
    game.debug_mode = False
    game.grid = []
    game.gridlist = []
    for y in range( math.ceil(settings["resolution"][1]/settings["tilesize"]) ):
        game.grid.append([]) #add first row
        for x in range( math.ceil(settings["resolution"][0]/settings["tilesize"]) ):
            if y==0 or x==0 or x==math.ceil(settings["resolution"][0]/settings["tilesize"])-1 or y==math.ceil(settings["resolution"][1]/settings["tilesize"])-1:
                game.grid[y].append( Square(x=x, y=y, isStand = 0) )
            else:
                game.grid[y].append( Square(x=x, y=y, isStand = 1) )
            game.gridlist.append( game.grid[y][x] )

    game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30

    game.teens = []
    game.teens.append( Character( name = "Adam", x = 3, y = 3) )
    game.state = "waiting"
    game.dooms = []
    game.dooms.append( Slasher(name="Slasher", x=6, y=6) )
