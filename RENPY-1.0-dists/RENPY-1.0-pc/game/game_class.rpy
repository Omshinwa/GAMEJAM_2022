##########SET UP THE BOARD###############
init offset = -1
init python:
    def gridAZ(game, x):
        return game.grid[ ord(x[0])-65 ][int(x[1])]

    def id2pos(x):
        return int(x * settings["tilesize"])

    def pos2id(x):
        return int(x / settings["tilesize"])

    def getMousePos():
        x, y = pygame.mouse.get_pos()
        store.mousex = x
        store.mousey = y
        print(x,y)

    def getMouseId():
        x, y = pygame.mouse.get_pos()
        store.mousexid = pos2id(x)
        store.mouseyid = pos2id(y)
        print(x,y)

    class Character:
        # init method or constructor
        def __init__(self, name, x, y):
            self.name = name
            self.x = x
            self.y = y
            self.img = {}
            self.AP = 1 #How much AP does it have?

            self.img.idle = name + "-idle.png"
            self.img.hover = name + "-hover.png"
            self.img.premove = name + "-premove.png"
            self.img.noAP = name + "-noAP.png"
            self.img.dead = name + "-dead.png"

            self.stat = {}
            self.stat.vis = 8
            self.stat.move = 3

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
                game.premoving_where = game.inrange2(self.x, self.y, self.stat.move)

        def move(self, cell):
            if cell.occupied == 0:
                game.grid[self.y][self.x].occupied = 0
                self.x = cell.x
                self.y = cell.y
                game.grid[self.y][self.x].occupied = 1
                game.updateVision()
                game.premoving_who = ""
                game.premoving_where = ""
                game.state = "waiting"
                self.removeAP(1)
                game.grid[self.y][self.x].onEvent(game)

                if game.totalAP() <= 0:
                    game.turnChange()


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
            renpy.call("lab_doommove", self)

            #some complicated pathfinding
