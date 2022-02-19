style debug_text2 is text:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
    color "#FFFF00"

label lab_tile_editor_render:
    show screen keybinds
    show screen sce_grid_editor
    show screen sce_walls_editor
    show screen sce_tile_editor_palette
    call screen sce_gameloop

screen sce_walls_editor():
    zorder 2

    for key, value in settings["lignes"].iteritems():
        $ x = int(key[1:3])
        $ y = ord(key[0])-65
        $ x2 = int(key[4:6])
        $ y2 = ord(key[3])-65
        frame:
            padding (0,0,0,0)
            if x==x2: #HORIZONTAL
                xysize 48, 4
                xpos int(x2 * settings["tilesize"])
                ypos int(y2 * settings["tilesize"])-2
            if y==y2: #HORIZONTAL
                xysize 4, 48
                xpos int(x2 * settings["tilesize"]) -2
                ypos int(y2 * settings["tilesize"])
            if value == 1:
                background Solid( "#808080" )
            if value == 2:
                background Solid( "#EEEEEE" )
            if value == 3:
                background "game-UI/door-open.png"

screen sce_grid_editor():

    for row in game.grid:
        for cell in row:
            frame:
                xpos int(cell.x * settings["tilesize"])
                ypos int(cell.y * settings["tilesize"])
                xysize int(settings["tilesize"]), int(settings["tilesize"])
                background cell.sprite()
            
    button:
        xysize (settings["mapsize"][0]+1) * settings["tilesize"], settings["mapsize"][1] * settings["tilesize"]
        action Jump("label_draw_on_tile")

    for row in game.grid:
        for cell in row:
            frame:
                padding (0,0,0,0)
                xpos int(cell.x * settings["tilesize"])
                ypos int(cell.y * settings["tilesize"])
                xysize int(settings["tilesize"]), int(settings["tilesize"])
                background cell.sprite()
                if game.state == "debug_tile_id":
                    text str(cell.type) size 25 style "debug_text2"
                if game.state == "debug_grillage":
                    frame:
                        background "game-UI/cell-grille.png"
                if game.debug_mode:
                    text chr(ord('@')+cell.y+1) + str(cell.x) size 30*settings["tilesize"]/96 style "debug_text"
                    text str(cell.y) + str(cell.x) size 20*settings["tilesize"]/96 ypos 30 style "debug_text"

        if debug_.draw_mode != "tile" and debug_.previous_tile:
            frame:
                background "game-UI/debug-select_ligne.png"
                xpos int(debug_.previous_tile[1:3]) * settings["tilesize"]
                ypos (ord(debug_.previous_tile[0])-65 ) * settings["tilesize"]

screen sce_tile_editor_palette():
    zorder 3

    frame:
        xpos (settings["mapsize"][0]) * settings["tilesize"]
        xsize settings["ui-size"] * settings["tilesize"]
        background Solid("#222")


        ####              TILES            #####
        for i, cell in enumerate(settings["tiletype"]):
            frame:
            # imagebutton:
                xpadding 0
                ypadding 0
                xpos i%6 * settings["tilesize"]
                ypos int(i/6) * settings["tilesize"]
                xysize settings["tilesize"], settings["tilesize"]
                background cell["img_idle"]
                if cell["type"] == debug_.tilebrush:
                    frame:
                        background "game-UI/debug-select-tilebrush.png"
                        xysize settings["tilesize"], settings["tilesize"]

                if game.state == "debug_tile_id":
                    text str(cell["type"]) size 25 style "debug_text2"
                # background Solid("#FFF000")

        button:
            xpos 0
            ypos 0
            xysize 6* settings["tilesize"],  7 * settings["tilesize"]
            action Jump("label_choose_tile_brush")
            background Solid("#f005")

        text "layer:" style "classicfont" yalign 0.6 xalign 0.0
        text "mode:" style "classicfont" yalign 0.7 xalign 0.0

        button:
            xalign 0.3
            yalign 0.64
            if debug_.draw_mode == "tile":
                background Solid("#FFFAAA")
            else:
                background Solid("#808080")
            text "TILE" size 30 style "debug_text"
            action SetVariable("debug_.draw_mode", "tile")

        button:
            xalign 1.0
            yalign 0.64
            if debug_.draw_mode == "wall":
                background Solid("#FFFAAA")
            else:
                background Solid("#808080")
            text "wall" size 30 style "debug_text"
            action SetVariable("debug_.draw_mode", "wall")

#########             doors             #################
        fixed:
            ypos 620
            
            button:
                xalign 0.0
                xsize 100
                ysize 50
                if debug_.draw_mode == "closed_door":
                    background Solid("#FFFAAA")
                else:
                    background Solid("#808080")
                text "open door" size 20 style "debug_text" xalign 0.5 yalign 0.5
                action SetVariable("debug_.draw_mode", "closed_door")

            button:
                xalign 0.5
                xsize 100
                ysize 50
                if debug_.draw_mode == "open_door":
                    background Solid("#FFFAAA")
                else:
                    background Solid("#808080")
                text "closed door" size 20 style "debug_text" xalign 0.5 yalign 0.5
                action SetVariable("debug_.draw_mode", "open_door")

            button:
                xalign 1.0
                xsize 100
                ysize 50
                if debug_.draw_mode == "secret_door":
                    background Solid("#FFFAAA")
                else:
                    background Solid("#808080")
                text "secret door" size 20 style "debug_text" xalign 0.5 yalign 0.5
                action SetVariable("debug_.draw_mode", "secret_door")

        text "display:" style "classicfont" yalign 0.89 xalign 0.0

        button:
            xalign 0.5
            yalign 0.90
            text "TILE ID" size 30 style "debug_text"
            if game.state == "debug_tile_id":
                background Solid("#FF00B0")
                action SetVariable("game.state", "debug")
            else:
                background Solid("#808080")
                action SetVariable("game.state", "debug_tile_id")

        button:
            xalign 1.0
            yalign 0.90
            text "GRID" size 30 style "debug_text"
            if game.state == "debug_grillage":
                background Solid("#FF00B0")
                action SetVariable("game.state", "debug")
            else:
                background Solid("#808080")
                action SetVariable("game.state", "debug_grillage")

        button:
            xalign 0.5
            yalign 0.99
            text "EXPORT ALL" size 30 style "debug_text"
            background Solid("#5080FF")
            action Jump("label_export_tilemap")
