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

    lauren = Character( name = "lauren", x = 2, y = 6)
    game.teens.append( lauren )
    william = Character( name = "william", x = 2, y = 2)
    game.teens.append( william )
    game.state = "waiting"
    # slasher = Slasher(name="Slasher", x=6, y=6)
    # game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=10, y=10)
    game.dooms.append( slasher2 )

    game.updateVision()
