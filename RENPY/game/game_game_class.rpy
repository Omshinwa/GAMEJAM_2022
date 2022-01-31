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

        def gridAZ(self, x):
            return self.grid[ ord(x[0])-65 ][int(x[1:])]

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

        def isCrossable(self,x2,y2,x = "bite",y = "bite", ifdoom = True, ifwalls=True):
            if self.grid[y2][x2].isStand == 0:
                return False
            if ifdoom:
                if self.grid[y2][x2].occupied == "doom":
                    return False

            if ifwalls:
                if x != "bite":
                    if x<10:
                        firstpart = chr(ord('@')+y+1) + "0" + str(x)
                    else:
                        firstpart = chr(ord('@')+y+1) + str(x)
                    if x2<10:
                        secondpart = chr(ord('@')+y2+1) + "0" + str(x2)
                    else:
                        secondpart = chr(ord('@')+y2+1) + str(x2)
                    name = firstpart + secondpart
                    if name in settings["walls"]:
                        return False

            return True

        def inrange2(self, x, y, howfar, ifdoom = True, ifwalls=True):
            def recursion(self, x, y, howfar, dict):
                if y>=0 and x>=0 and y<game.maxY and x<game.maxX:
                    if ifdoom == True:
                        if game.grid[y][x].occupied == 0:
                            dict[y,x] = game.grid[y][x]
                    else:
                        if game.grid[y][x].occupied == 0 or game.grid[y][x].occupied == "doom":
                            dict[y,x] = game.grid[y][x]
                if (howfar > 0):
                    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                        if self.isCrossable(x+direction[0],y+direction[1],x,y,ifdoom,ifwalls):
                            recursion(self,x+direction[0], y+direction[1] ,howfar - 1,dict)
            dict = {}
            recursion(self,x, y, howfar,dict)
            dict[x,y] = game.grid[y][x]
            return list(dict.values())


        def updateVision(self):
            for case in game.gridlist:
                case.visibility = 0
            for teen in game.teens:
                if teen.isAlive:
                    for case in self.inrange( teen.x , teen.y , teen.stat.vis):
                        case.visibility = 0
            for teen in game.teens:
                if teen.isAlive:
                    for case in self.inrange( teen.x , teen.y , teen.stat.vis):
                        if case.x == teen.x and case.y == teen.y:
                            case.visibility = 1
                        elif case.isStand == 0:
                            case.visibility = 0
                        else:
                            difx = case.x - teen.x
                            dify = case.y - teen.y
                            maxi = max(abs(difx),abs(dify))
                            if maxi==0:
                                ratio = (0,0)
                            else:
                                ratio =(difx*1.0/maxi, dify*1.0/maxi)
                            for i in range(abs(difx) + abs(dify)):
                                yyy = teen.y + ratio[1]*(i+1)
                                xxx = teen.x + ratio[0]*(i+1)
                                if yyy>=0 and xxx>=0 and yyy<game.maxY and xxx<game.maxX:
                                    if game.grid[ int(yyy) ][ int(xxx) ].isStand == 0:
                                        # case.visibility = 0
                                        break
                                    if game.grid[ math.ceil(yyy) ][ math.ceil(xxx) ].isStand == 0:
                                        # case.visibility = 0
                                        break
                                    if xxx == case.x and yyy == case.y:
                                        case.visibility = 1
                                        break
