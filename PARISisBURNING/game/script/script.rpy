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
    game = Game()

    #create characters

    lauren = game.teens[0]
    william = game.teens[1]
    game.updateVision()

    game.grid[7][12].onFire = -1

return


label lab_credit:
    "thanks to the renpy discord community for their help (tomrenpy, AxelKong"
    "sound people:
    https://bigsoundbank.com/detail-0495-steps-in-the-mud.html
    https://www.zapsplat.com/music/water-from-bucket-throw-splash-splat-on-concrete-ground-1/"