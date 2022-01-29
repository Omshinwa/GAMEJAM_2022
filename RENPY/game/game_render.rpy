label lab_render:
    call screen sce_grid
    ""
    ""
    ""

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
    pass

screen sce_grid:
    for cell in game.gridlist:
        frame:
            xpadding 0
            ypadding 0
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            if (cell.x + cell.y)%2 == 0:
                background Solid( "#FFFFFF" )
            else:
                background Solid( "#000000" )
            imagebutton:
                xpos 0
                ypos 0
                idle "game-UI/cell-idle.png"
                    #FUCKING REMEMBER INT = PIXEL, FLOAT = RAPPORT
                hover "img_cell_hover"
                xysize int(settings["tilesize"]), int(settings["tilesize"])

                if renpy.get_screen("say"):
                    sensitive False
                else:
                    sensitive True

                action NullAction()

            if game.debug_mode:
                    text chr(ord('@')+cell.y+1) + str(cell.x) size 30
                    text str(cell.y) + str(cell.x) size 20 ypos 30
                    # xpos settings["tilesize"]/2

        # imagebutton:
        #     xysize int(settings["tilesize"]), int(settings["tilesize"])
        #     xpos int(cell.x * settings["tilesize"])
        #     ypos int(cell.y * settings["tilesize"])
        #     idle "game-UI/cell-idle.png"
        #     hover "img_cell_hover"
        #     action NullAction()
        #
        # if game.debug_mode:
        #     button xpos int(cell.x * settings["tilesize"]) ypos int(cell.y * settings["tilesize"]):
        #         text chr(ord('@')+cell.y+1) + str(cell.x) size 30
        #         text str(cell.y) + str(cell.x) size 20 ypos 30
        #             # xpos settings["tilesize"]/2
