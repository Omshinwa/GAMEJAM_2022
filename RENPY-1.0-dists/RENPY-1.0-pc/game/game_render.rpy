style debug_text is text:
    outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
    color "#FFFFFF"

label lab_render:
    show screen sce_grid
    show screen sce_doom
    show screen sce_char
    show screen sce_fog

    call screen sce_gameloop

image img_cell_hover:
    "game-UI/cell-hover-01.png"
    pause(0.1)
    "game-UI/cell-hover-02.png"
    pause(0.1)
    "game-UI/cell-hover-03.png"
    pause(0.1)
    "game-UI/cell-hover-04.png"
    pause(0.1)
    "game-UI/cell-hover-05.png"
    pause(0.1)
    repeat

screen sce_gameloop():
    pass

screen sce_char():
    zorder 1
    #First draw the dead people
    for teen in game.teens:
        if teen.isAlive == 0:
            imagebutton:
                xpos id2pos(teen.x)
                ypos id2pos(teen.y)
                idle teen.sprite()
                action NullAction()
                sensitive False

    for teen in game.teens:
        if teen.isAlive == 1:
            imagebutton:
                xpos id2pos(teen.x)
                ypos id2pos(teen.y)
                idle teen.sprite()
                if teen.AP > 0 :
                    hover teen.img.hover
                if renpy.get_screen("say"):
                    sensitive False
                else:
                    sensitive True
                action Function(teen.premove)

screen sce_doom():

    zorder 2

    for doom in game.dooms:
        imagebutton:
            xpos id2pos(doom.x)
            ypos id2pos(doom.y)
            idle doom.sprite()
            # hover doom.hover()
            action NullAction()
            sensitive game.grid[doom.y][doom.x].visibility


screen sce_fog():
    zorder 2
    for cell in game.gridlist:
        frame:
            padding (0,0,0,0)
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            if cell.visibility == 0:
                background Solid( "#00000080" )
            else:
                background Solid( "#FF000020" )

            if game.debug_mode:
                text chr(ord('@')+cell.y+1) + str(cell.x) size 30*settings["tilesize"]/96 style "debug_text"
                text str(cell.y) + str(cell.x) size 20*settings["tilesize"]/96 ypos 30 style "debug_text"

#EXAMPLE DE COMPOSITE QUI MARCHE
# return Composite(
#         (96, 96),
#         (0, 0), img,
#         (0, 0), Transform( self.img.unstand , alpha = 0.5  ))

screen sce_grid():
    for cell in game.gridlist:
        imagebutton:
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            idle cell.sprite()

    if game.state=="moving":
        button:
            xysize int(settings["resolution"][0]), int(settings["resolution"][1])
            action [SetVariable("game.state", "waiting"), SetVariable("game.premoving_where", "")]
    for cell in game.premoving_where:
        imagebutton:
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            hover game.premoving_who.img.idle
            idle "game-UI/cell-blank.png"
            action Function(game.premoving_who.move, cell=cell)

    text game.state size 80 color "#FF0000"
    text "SCORE:"+str(game.score) size 40 color "#FF0000" xalign 1.0
