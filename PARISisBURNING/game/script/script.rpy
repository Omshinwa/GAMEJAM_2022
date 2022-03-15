label start:
    show screen keybinds
    call load("000")

label load(filename):
    $ game = Game(filename)
    show screen sce_grid
    show screen sce_doom
    show screen sce_char
    show screen sce_fog
    show screen sce_walls
    show screen sce_UI
    $ game.updateVision()
    $ renpy.call("lab_"+filename+"_start")
    jump lab_render

#tout ce qui est en dessous c de moi
screen keybinds():
    key 'K_F2' action Function(debugmode)

###############################################################################**
#### INITIALIZE THE GAME BOARD
#################################################################################


label lab_credit:
    "thanks to the renpy discord community for their help (tomrenpy, AxelKong, Pinky!, Fen (Somniarre)"
    "sound people:
    https://bigsoundbank.com/detail-0495-steps-in-the-mud.html
    https://www.zapsplat.com/music/water-from-bucket-throw-splash-splat-on-concrete-ground-1/"