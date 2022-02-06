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

    #create characters
    lauren = Character( game, name = "lauren", x = 2, y = 7)
    game.teens.append( lauren )
    william = Character( game, name = "william", x = 11, y = 6)
    game.teens.append( william )
    darryl = Character( game, name = "darryl", x = 15, y = 4)
    game.teens.append( darryl )
    kayleigh = Character( game, name = "kayleigh", x = 4, y = 8)
    game.teens.append( kayleigh )

    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=12, y=8, canOpenDoors= True)
    game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=10, y=11, canOpenDoors= True)
    game.dooms.append( slasher2 )
    game.updateVision()

    william.inventory.append( Bucket() )
return
