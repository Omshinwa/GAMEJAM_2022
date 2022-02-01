#INITIALIZE THE BOARD
init python:

    settings["events"] = merge_two_dicts( settings["events_fyn"], settings["events_madi"])

    game = Game()
    game.maxY =  math.ceil(settings["resolution"][1]/settings["tilesize"])-1
    game.maxX = math.ceil(settings["resolution"][0]/settings["tilesize"])-1
    for y in range( game.maxY+1 ):
        game.grid.append([]) #add first row
        for x in range( game.maxX+1 ):
            try:
                settings["tilemap"][y][x]
            except IndexError:
                game.grid[y].append( Square(x=x, y=y, type = 0 ) )
            else:
                game.grid[y].append( Square(x=x, y=y, type = settings["tilemap"][y][x] ) )
            game.gridlist.append( game.grid[y][x] )

    # game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30

    def gride(y,x):
        return game.grid[y][x]

    lauren = Character( name = "lauren", x = 2, y = 6)
    game.teens.append( lauren )
    william = Character( name = "william", x = 17, y = 8)
    game.teens.append( william )
    darryl = Character( name = "darryl", x = 15, y = 4)
    game.teens.append( darryl )
    kayleigh = Character( name = "kayleigh", x = 5, y = 8)
    game.teens.append( kayleigh )

    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=12, y=12)
    game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=10, y=11)
    game.dooms.append( slasher2 )
    game.updateVision()
