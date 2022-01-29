label lab_render:
    show screen sce_grid
    show screen sce_doom
    show screen sce_fog
    call screen sce_char

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

screen sce_char:
    zorder 1
    for teen in game.teens:
        imagebutton:
            xpos id2pos(teen.x)
            ypos id2pos(teen.y)
            idle teen.sprite()
            hover teen.img.hover
            action Function(teen.premove)

screen sce_doom:

    if game.grid[game.dooms[0].y][game.dooms[0].x].visibility == 0:
        zorder -6
    else:
        zorder 1

    for doom in game.dooms:
        imagebutton:
            xpos id2pos(doom.x)
            ypos id2pos(doom.y)
            idle doom.sprite()
            # hover doom.hover()
            action NullAction()
            sensitive game.grid[doom.y][doom.x].visibility


screen sce_fog:
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
                text chr(ord('@')+cell.y+1) + str(cell.x) size 30
                text str(cell.y) + str(cell.x) size 20 ypos 30

#EXAMPLE DE COMPOSITE QUI MARCHE
# return Composite(
#         (96, 96),
#         (0, 0), img,
#         (0, 0), Transform( self.img.unstand , alpha = 0.5  ))

screen sce_grid:

    for cell in game.gridlist:
        frame:
            padding (0,0,0,0)
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            if (cell.x + cell.y)%2 == 0:
                background Solid( "#FFFFFF" )
            else:
                background Solid( "#000000" )
            imagebutton:
                idle cell.sprite()
                if game.state == "moving" and (cell.empty == 0 or cell.empty == "Slasher"):
                    hover game.premoving_who.img.idle
                    action Function(game.premoving_who.move, cell=cell)
                else:
                    hover cell.img.hover
                    action NullAction()
                xysize int(settings["tilesize"]), int(settings["tilesize"])
                sensitive True
    text game.state size 80 color "#FF0000"
