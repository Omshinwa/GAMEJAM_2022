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
    lauren = Character( game, name = "lauren", x = 16, y = 6)
    game.teens.append( lauren )
    william = Character( game, name = "william", x = 17, y = 6)
    game.teens.append( william )
    paula = Character( game, name = "paula", x = 16, y = 8)
    game.teens.append( paula )
    gwenael = Character( game, name = "gwenael", x = 17, y = 7)
    game.teens.append( gwenael )
    # darryl = Character( game, name = "darryl", x = 16, y = 6)
    # game.teens.append( darryl )
    # kayleigh = Character( game, name = "kayleigh", x = 15, y = 7)
    # game.teens.append( kayleigh )

    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=21, y=7, canOpenDoors= True)
    game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=22, y=7, canOpenDoors= True)
    game.dooms.append( slasher2 )
    game.updateVision()

    game.grid[7][12].onFire = -1

    william.inventory.append( Items("Bucket") )
    lauren.inventory.append( Items("Bucket") )
    gwenael.inventory.append( Items("Bucket") )
    paula.inventory.append( Items("Bucket") )
    # darryl.inventory.append( Bucket() )
    # kayleigh.inventory.append( Bucket() )
return


label lab_credit:
    "thanks to the renpy discord community for their help (tomrenpy, AxelKong"
    "sound people:
    https://bigsoundbank.com/detail-0495-steps-in-the-mud.html
    https://www.zapsplat.com/music/water-from-bucket-throw-splash-splat-on-concrete-ground-1/"