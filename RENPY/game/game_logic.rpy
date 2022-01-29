##########SET UP THE BOARD###############

init python:
    import math

    settings = {}
    settings["tilesize"] = 96.0 #in pixel
    settings["resolution"] = (1920.0,1080.0)

    # def id2pos(x):
    #     return x * settings["tilesize"]
    #     pass

    def pos2id(x):
        return x / settings["tilesize"]

    class Square:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.xpos = x * settings["tilesize"]
            self.ypos = y * settings["tilesize"]
        def __repr__(self):
            return " (x" +str(self.x)+ ":y" +str(self.y)+") "

    class Person:

        # init method or constructor
        def __init__(self, name):
            self.name = name

        # Sample Method
        def say_hi(self):
            print('Hello, my name is', self.name)

    class Character:

        def __init__(self, name):

            self.xid = 0
            self.xid = 0


    game = {}
    game.debug_mode = False
    game.grid = []
    game.gridlist = []
    for y in range( math.ceil(settings["resolution"][1]/settings["tilesize"]) ):
        game.grid.append([]) #add first row
        for x in range( math.ceil(settings["resolution"][0]/settings["tilesize"]) ):
            game.grid[y].append( Square(x, y) )
            game.gridlist.append( game.grid[y][x] )

    game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30
