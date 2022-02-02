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

        def interaction(x,y):
            return False

        def gridAZ(self, x):
            return self.grid[ ord(x[0])-65 ][int(x[1:])]

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
                            if game.grid[yi + y][xi + x].isDark:
                                dict_hide[yi + y,xi + x] = game.grid[yi + y][xi + x]
                            else:
                                dict[yi + y,xi + x] = game.grid[yi + y][xi + x]
            return list(dict.values())

        def isCrossable(self,x2,y2,x = "bite",y = "bite", ifdoom = True, ifwalls=True, ifstoppable=True, ifdoors=True):
            if x2<0 or y2<0 or x2>game.maxX or y2>game.maxY:
                return False

            if ifstoppable:
                if self.grid[y2][x2].isStand == 0:
                    return False
            if ifdoom:
                if self.grid[y2][x2].occupied == "doom":
                    return False

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
                name2 = secondpart + firstpart
                if ifwalls:
                    if name in settings["lignes"] and settings["lignes"][name] == 1:
                        return False
                    if name2 in settings["lignes"] and settings["lignes"][name2] == 1:
                        return False
                if ifdoors:
                    if name in settings["lignes"] and settings["lignes"][name] == 2:
                        return False
                    if name2 in settings["lignes"] and settings["lignes"][name2] == 2:
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
                        # elif case.isDark == 0:
                        #     case.visibility = 0
                        else:
                            difx = case.x - teen.x
                            dify = case.y - teen.y
                            maxi = max(abs(difx),abs(dify))
                            if maxi==0:
                                ratio = (0,0)
                            else:
                                ratio =(difx*1.0/maxi, dify*1.0/maxi)
                            for i in range( maxi ):
                                yyy = teen.y + ratio[1]*(i+1)
                                xxx = teen.x + ratio[0]*(i+1)
                                if yyy>=0 and xxx>=0 and yyy<game.maxY and xxx<game.maxX:
                                    yy = teen.y + ratio[1]*(i)
                                    xx = teen.x + ratio[0]*(i)

                                    if game.grid[ int(yyy) ][ int(xxx) ].blockVision:
                                        # case.visibility = 0
                                        break
                                    # if game.grid[ math.ceil(yyy) ][ math.ceil(xxx) ].blockVision:
                                    #     # case.visibility = 0
                                    #     break

                                    #check for walls block visibility:
                                    if abs(int(xxx) - int(xx)) + abs(int(yyy) - int(yy)) == 2 :
                                        # ON FAIT LA TRANSITION PUTAIN
                                        a = not game.isCrossable(x2=int(xx),y2=int(yyy),x= int(xx), y=int(yy), ifdoom = False, ifwalls=True, ifstoppable=False)
                                        b = not game.isCrossable(x2=int(xxx),y2=int(yyy),x= int(xx), y=int(yyy), ifdoom = False, ifwalls=True, ifstoppable=False)

                                        c = not game.isCrossable(x2=int(xxx),y2=int(yy),x= int(xx), y=int(yy), ifdoom = False, ifwalls=True, ifstoppable=False)
                                        d = not game.isCrossable(x2=int(xxx),y2=int(yyy),x= int(xxx), y=int(yy), ifdoom = False, ifwalls=True, ifstoppable=False)
                                        if (a or b) and (c or d):
                                            break

                                    if not game.isCrossable(x2= int(round(xxx)),y2= int(round(yyy)),x= int( round(xx) ), y= int( round(yy) ), ifdoom = False, ifwalls=True, ifstoppable=False):
                                        break
                                    elif not game.isCrossable(x2=int(xxx),y2=int(yyy),x=int( teen.x + ratio[0]*(i) ), y=int( teen.y + ratio[1]*(i) ), ifdoom = False, ifwalls=True, ifstoppable=False):
                                        break
                                    elif not game.isCrossable(x2=math.ceil(xxx),y2=math.ceil(yyy),x=math.ceil( teen.x + ratio[0]*(i) ), y=math.ceil( teen.y + ratio[1]*(i) ), ifdoom = False, ifwalls=True, ifstoppable=False):
                                        break

                                    if xxx == case.x and yyy == case.y:
                                        case.visibility = 1
                                        break
