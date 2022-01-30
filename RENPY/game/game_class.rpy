init python:
    class Game:

        def __init__(self):
            self.ui = {}
            self.grid = []
            self.gridlist = []
            self.debug_mode = False
            self.teens = []
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

        def inrange2(self, x, y, howfar):
            def recursion(self, x, y, howfar, dict):
                if y>=0 and x>=0 and y<game.maxY and x<game.maxX:
                    dict[y,x] = game.grid[y][x]
                if (howfar > 0):
                    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                        recursion(self,x+direction[0], y+direction[1] ,howfar - 1,dict)
            dict = {}
            recursion(self,x, y, howfar,dict)
            return list(dict.values())

        def updateVision(self):
            for case in game.gridlist:
                case.visibility = 0
            for teen in game.teens:
                for case in self.inrange2( teen.x , teen.y , teen.stats.vis):
                    case.visibility = 1


    game = Game()
    game.maxY =  math.ceil(settings["resolution"][1]/settings["tilesize"])-1
    game.maxX = math.ceil(settings["resolution"][0]/settings["tilesize"])-1
    for y in range( game.maxY+1 ):
        game.grid.append([]) #add first row
        for x in range( game.maxX+1 ):
            game.grid[y].append( Square(x=x, y=y, type = settings["tilemap"][y][x] ) )
            game.gridlist.append( game.grid[y][x] )

    game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30

    game.teens.append( Character( name = "lauren", x = 3, y = 3) )
    game.teens.append( Character( name = "william", x = 8, y = 8) )
    game.state = "waiting"
    game.dooms = []
    game.dooms.append( Slasher(name="Slasher", x=6, y=6) )
    game.updateVision()
