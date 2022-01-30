#INITIALIZE THE BOARD
init python:

    settings["events"] = merge_two_dicts( settings["events_fyn"], settings["events_madi"])
    settings["switches"] = merge_two_dicts( settings["switches_fyn"], settings["switches_madi"])

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

    lauren = Character( name = "lauren", x = 3, y = 3)
    game.teens.append( lauren )
    william = Character( name = "william", x = 8, y = 8)
    game.teens.append( william )
    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=6, y=6)
    game.dooms.append( slasher )
    game.updateVision()
