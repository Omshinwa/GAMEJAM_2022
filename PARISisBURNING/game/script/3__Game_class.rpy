init offset = -1
init python:
    class Game:

        def __init__(self):
            self.ui = {}
            self.grid = []
            self.debug_mode = False
            self.teens = []
            self.dooms = []
            self.premoving_who = ""
            self.premoving_where = {}
            self.score = 0
            self.actions = []
            
            self.maxY = settings["mapsize"][1]
            self.maxX = settings["mapsize"][0]

            #create grid
            for y in range( self.maxY+1 ):
                self.grid.append([]) #add first row
                for x in range( self.maxX+1 ):
                    try:
                        settings["tilemap"][y][x]
                    except IndexError:
                        self.grid[y].append( Square(x=x, y=y, type = 0 ) )
                    else:
                        self.grid[y].append( Square(x=x, y=y, type = settings["tilemap"][y][x] ) )

            #create actions for doors
            for key, value in settings["lignes"].iteritems():
                if value == 2 or value == 3:

                    x,y,x2,y2 = AZto09(key)
                    self.grid[y][x].onAction.append( Item_Action(name="door", isItem="False",rangeOfActivation=0,text="DOOR",label="lab_action_door", variables=key) )
                    self.grid[y2][x2].onAction.append(  Item_Action(name="door", isItem="False",rangeOfActivation=0,text="DOOR",label="lab_action_door", variables=key) )

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

        @staticmethod
        def squareExist(y,x):
            if x>=0 and x< settings["mapsize"][0] and y>=0 and y< settings["mapsize"][1]:
                return True
            else:
                return False

        def isCrossable(self,x2,y2,x = "bite",y = "bite", iftile = True, ifwall=True, ifdoor=True, ifteen=True, ifdoom = True, canOpenDoors=False, lastMovement=False):
            #ifdoor = False allow to cross through all doors
            #if
            if iftile:
                if self.grid[y2][x2].isStand == 0:
                    return False

            if x2<0 or y2<0 or x2>game.maxX or y2>game.maxY:
                return False

            if lastMovement: # should only check at the end of the loop
                if self.grid[y2][x2].occupied != 0:
                    return False
            if ifdoom:
                if self.grid[y2][x2].occupied == "doom":
                    return False
            if ifteen:
                if self.grid[y2][x2].occupied == "teen":
                    return False

            if x != "bite": #ON A BESOIN DE LA POSITION DE DEPART POUR CALCULER LES MURS
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
                namelist = [name,name2]
                if ifwall:
                    for cell in namelist:
                        if cell in settings["lignes"] and settings["lignes"][cell] == 1:
                            return False
                if ifdoor:
                    for cell in namelist:
                        if cell in settings["lignes"] and settings["lignes"][cell] == 2:
                            if canOpenDoors: #can that door be openable?

                            #EDGE CASE WHERE HE CAN OPEN EVEN THOUGH THERES A DOOM NEXT DOOR
                                a = game.grid[y][x].occupied=="teen" or game.grid[y][x].isStand == 0
                                b = game.grid[y2][x2].occupied=="teen" or game.grid[y2][x2].isStand == 0
                                if a or b:
                                    return False
                            else:
                                return False


            return True

        def isThereAcadaver(self, case):
            for teen in self.teens:
                if teen.isAlive == 0:
                    if teen.x == case.x and teen.y == case.y:
                        return True
            return False

        def inrange2(self, x, y, howfar, **kwargs): #used for showing the range of the player mov
            def recursion(self, x, y, howfar, dict):
                if game.squareExist(x=x,y=y):
                    if game.grid[y][x].occupied == 0:
                        dict[y,x] = game.grid[y][x]
                    #the player can walk into a surprise doom
                    if game.grid[y][x].occupied == "doom" and game.grid[y][x].visibility==0:
                        dict[y,x] = game.grid[y][x]

                if (howfar >= 1):
                    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                        if self.isCrossable(x2=x+direction[0],y2=y+direction[1],x=x,y=y,lastMovement= (howfar==1), **kwargs ): # 
                            recursion(self,x+direction[0], y+direction[1] ,howfar - 1,dict)

            dict = {}
            recursion(self,x, y, howfar,dict)
            dict[x,y] = game.grid[y][x]
            return list(dict.values())


        def updateVision(self):
            for row in game.grid:
                for case in row:
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
                                        a = not game.isCrossable(x2=int(xx),y2=int(yyy),x= int(xx), y=int(yy), ifdoom = False, iftile=False)
                                        b = not game.isCrossable(x2=int(xxx),y2=int(yyy),x= int(xx), y=int(yyy), ifdoom = False, iftile=False)

                                        c = not game.isCrossable(x2=int(xxx),y2=int(yy),x= int(xx), y=int(yy), ifdoom = False, iftile=False)
                                        d = not game.isCrossable(x2=int(xxx),y2=int(yyy),x= int(xxx), y=int(yy), ifdoom = False, iftile=False)
                                        if (a or b) and (c or d):
                                            break

                                    if not game.isCrossable(x2= int(round(xxx)),y2= int(round(yyy)),x= int( round(xx) ), y= int( round(yy) ), ifdoom = False, iftile=False):
                                        break
                                    elif not game.isCrossable(x2=int(xxx),y2=int(yyy),x=int( teen.x + ratio[0]*(i) ), y=int( teen.y + ratio[1]*(i) ), ifdoom = False, iftile=False):
                                        break
                                    elif not game.isCrossable(x2=math.ceil(xxx),y2=math.ceil(yyy),x=math.ceil( teen.x + ratio[0]*(i) ), y=math.ceil( teen.y + ratio[1]*(i) ), ifdoom = False, iftile=False,):
                                        break

                                    if xxx == case.x and yyy == case.y:
                                        case.visibility = 1
                                        break
        def doommove(self):
            for doom in self.dooms:
                print("cmb:" + str(len(self.dooms)))
                doom.move()
            renpy.jump("lab_turnChange")

        