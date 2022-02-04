label start:
show screen keybinds
call lab_initialize
jump lab_gameloop
return

#tout ce qui est en dessous c de moi
screen keybinds():
    key 'K_F2' action Function(debugmode)

###############################################################################**
#### INITIALIZE THE GAME BOARD
#################################################################################
label lab_initialize:
python:
    settings["events"] = merge_two_dicts( settings["events_fyn"], settings["events_madi"])

    game = Game()
    game.maxY =  settings["mapsize"][1]
    game.maxX = settings["mapsize"][0]
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

    # def gride(y,x):
    #     return game.grid[y][x]

    lauren = Character( name = "lauren", x = 2, y = 7)
    game.teens.append( lauren )
    william = Character( name = "william", x = 11, y = 6)
    game.teens.append( william )
    darryl = Character( name = "darryl", x = 15, y = 4)
    game.teens.append( darryl )
    kayleigh = Character( name = "kayleigh", x = 4, y = 8)
    game.teens.append( kayleigh )

    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=12, y=8, canOpenDoors= True)
    game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=10, y=11, canOpenDoors= True)
    game.dooms.append( slasher2 )
    game.updateVision()
return
