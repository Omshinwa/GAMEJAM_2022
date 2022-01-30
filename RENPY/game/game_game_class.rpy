init offset = -1
init python:
    class Game:

        def __init__(self):
            self.ui = {}
            self.grid = []
            self.gridlist = []
            self.debug_mode = False
            self.teens = []
            self.dooms = []
            self.premoving_who = ""
            self.premoving_where = {}
            self.score = 0
            pass

        def turnChange(self):
            self.updateVision()
            if self.state == "waiting":
                self.state = "doom"
                for doom in game.dooms:
                    doom.move()
                    self.score += 1
                    self.turnChange()

            elif self.state == "doom":
                self.state = "waiting"
                self.restore_totalAP()

        def restore_totalAP(self):
            for teen in self.teens:
                teen.AP = 1 * teen.isAlive

        def totalAP(self):
            totalAP = 0
            for teen in self.teens:
                totalAP += teen.AP
            return totalAP

        def inrange(self, x, y, howfar):
            dict = {}
            dict_hide={}
            for xi in range(-howfar ,howfar+1):
                range2 = abs(abs(xi)-howfar)
                for yi in range(-range2, range2+1):
                    if yi + y>=0 and xi + x>=0:
                        try:
                            game.grid[yi + y][xi + x]
                        except:
                            pass
                        else:
                            if game.grid[yi + y][xi + x].blockVision:
                                dict_hide[yi + y,xi + x] = game.grid[yi + y][xi + x]
                            else:
                                dict[yi + y,xi + x] = game.grid[yi + y][xi + x]
            return list(dict.values())

        def isCrossable(self,x,y):
            if self.grid[y][x].isStand == 0:
                return False
            if self.grid[y][x].occupied == "doom":
                return False
            return True

        def inrange2(self, x, y, howfar):
            def recursion(self, x, y, howfar, dict):
                if y>=0 and x>=0 and y<game.maxY and x<game.maxX:
                    if game.grid[y][x].occupied == 0:
                        dict[y,x] = game.grid[y][x]
                if (howfar > 0):
                    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                        if self.isCrossable(x+direction[0],y+direction[1]):
                            recursion(self,x+direction[0], y+direction[1] ,howfar - 1,dict)
            dict = {}
            recursion(self,x, y, howfar,dict)
            return list(dict.values())

        def updateVision(self):
            for case in game.gridlist:
                case.visibility = 0
            for teen in game.teens:
                for case in self.inrange( teen.x , teen.y , teen.stats.vis):
                    case.visibility = 1

        def gridAZ(self, x):
            return self.grid[ ord(x[0])-65 ][int(x[1])]
