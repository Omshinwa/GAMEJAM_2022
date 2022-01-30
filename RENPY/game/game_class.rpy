##########SET UP THE BOARD###############
init offset = -1
init python:
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
            self.stats = {}
            self.stats.vis = 8
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
                game.premoving_where = game.inrange2(self.x, self.y, 3)

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
                game.grid[self.y][self.x].onEvent()

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
            game.grid[self.y][self.x].occupied = 0

            self.x = self.x + random.randint(-1,1)
            if self.x < 0: self.x = 0
            if self.x > game.maxX: self.x = game.maxX

            self.y = self.y + random.randint(-1,1)
            if self.y < 0: self.y = 0
            if self.y > game.maxX: self.y = game.maxY

            game.grid[self.y][self.x].occupied = 1
            for teen in game.teens:
                if self.x == teen.x and self.y == teen.y:
                    teen.isAlive = 0
                    game.grid[teen.y][teen.x].occupied = 0

            #some complicated pathfinding
