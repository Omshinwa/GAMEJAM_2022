style debug_text2 is text:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
    color "#FFFF00"

style char_editor_info_txt is text:
    font "IREADCASLON.TTF" size 30 color "#eee" antialias False 

label lab_tile_editor_render:
    show screen keybinds
    show screen sce_grid_editor
    show screen sce_walls_editor
    show screen sce_tile_editor_palette
    call screen sce_gameloop
    jump lab_tile_editor_render

screen sce_walls_editor():
    zorder 2

    for key, value in settings["line"].iteritems():
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
                
    ############################char
    if(debug_.draw_layer=="char"):
        for teen in game.teens:
            add teen.sprite() xpos id2pos(teen.x) ypos id2pos(teen.y)
        for doom in game.dooms:
            add doom.sprite() xpos id2pos(doom.x) ypos id2pos(doom.y)


screen sce_tile_editor_palette():
    zorder 3

    frame:
        xpos (settings["mapsize"][0]) * settings["tilesize"]
        xsize settings["ui-size"] * settings["tilesize"]
        background Solid("#222")

        ####              TILES            #####
        if (debug_.draw_layer == "map"):
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

        ####              characters            #####
        if (debug_.draw_layer == "char"):
            for i, cell in enumerate(debug_.charList):
                frame:
                # imagebutton:
                    xpadding 0
                    ypadding 0
                    xpos i%6 * settings["tilesize"]
                    ypos int(i/6) * settings["tilesize"]
                    xysize settings["tilesize"], settings["tilesize"]
                    background cell+"-idle.png"
                    if debug_.tilebrush == cell:
                        frame:
                            background "game-UI/debug-select-tilebrush.png"
                            xysize settings["tilesize"], settings["tilesize"]
            for i, cell in enumerate(debug_.doomList):
                frame:
                # imagebutton:
                    xpadding 0
                    ypadding 0
                    xpos i%6 * settings["tilesize"]
                    ypos (int(i/6)+6) * settings["tilesize"]
                    xysize settings["tilesize"], settings["tilesize"]
                    background cell+"-idle.png"
                    if debug_.tilebrush == cell:
                        frame:
                            background "game-UI/debug-select-tilebrush.png"
                            xysize settings["tilesize"], settings["tilesize"]


        button:
            xpos 0
            ypos 0
            xysize 6* settings["tilesize"],  7 * settings["tilesize"]
            action Jump("label_choose_tile_brush")
            background Solid("#f001")

        text "layer:" style "classicfont" ypos 460 xalign 0.0
        fixed:
            button:
                xalign 0.0
                ypos 490
                if debug_.draw_layer == "map":
                    background Solid("#5dff9b")
                else:
                    background Solid("#808080")
                text "MAP " size 30 style "debug_text"
                action [SetVariable("debug_.draw_layer", "map"),SetVariable("debug_.draw_mode", "tile")]
            button:
                xalign 0.45
                ypos 490
                if debug_.draw_layer == "char":
                    background Solid("#ff5151")
                else:
                    background Solid("#808080")
                text "CHAR" size 30 style "debug_text"
                action [SetVariable("debug_.draw_layer", "char") , SetVariable("debug_.draw_mode", "add") ]

            button:
                xalign 1.0
                ypos 490
                if debug_.draw_layer == "event":
                    background Solid("#ff4ad8")
                else:
                    background Solid("#808080")
                text "EVENT" size 30 style "debug_text"
                action SetVariable("debug_.draw_layer", "event")

            text "mode:" style "classicfont" yalign 0.7 xalign 0.0

        if (debug_.draw_layer == "map"):
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            button:
                xalign 0.3
                ypos 560
                if debug_.draw_mode == "tile":
                    background Solid("#FFFAAA")
                else:
                    background Solid("#808080")
                text "tile" size 30 style "debug_text"
                action SetVariable("debug_.draw_mode", "tile")

            button:
                xalign 0.8
                ypos 560
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


        if (debug_.draw_layer == "char"):
            # button:
            #     xalign 0.3
            #     ypos 560
            #     if debug_.draw_mode == "teen":
            #         background Solid("#FFFAAA")
            #     else:
            #         background Solid("#808080")
            #     text "teen" size 30 style "debug_text"
            #     action SetVariable("debug_.draw_mode", "teen")

            # button:
            #     xalign 0.8
            #     ypos 560
            #     if debug_.draw_mode == "slasher":
            #         background Solid("#FFFAAA")
            #     else:
            #         background Solid("#808080")
            #     text "slasher" size 30 style "debug_text"
            #     action SetVariable("debug_.draw_mode", "slasher")

            fixed:
                ypos 620
                
                button:
                    xalign 0.0
                    xsize 100
                    ysize 50
                    if debug_.draw_mode == "add":
                        background Solid("#FFFAAA")
                    else:
                        background Solid("#808080")
                    text "add/edit" size 20 style "debug_text" xalign 0.5 yalign 0.5
                    action SetVariable("debug_.draw_mode", "add")

                button:
                    xalign 0.5
                    xsize 100
                    ysize 50
                    if debug_.draw_mode == "delete":
                        background Solid("#FFFAAA")
                    else:
                        background Solid("#808080")
                    text "delete" size 20 style "debug_text" xalign 0.5 yalign 0.5
                    action SetVariable("debug_.draw_mode", "delete")

                # button:
                #     xalign 1.0
                #     xsize 100
                #     ysize 50
                #     if debug_.draw_mode == "secret_door":
                #         background Solid("#FFFAAA")
                #     else:
                #         background Solid("#808080")
                #     text "secret door" size 20 style "debug_text" xalign 0.5 yalign 0.5
                #     action SetVariable("debug_.draw_mode", "secret_door")

        # if (debug_.draw_layer == "event"):

        button:
            xalign 0.5
            yalign 0.99
            text "EXPORT ALL" size 30 style "debug_text"
            background Solid("#5080FF")
            action Jump("label_export_tilemap")


screen sce_char_editor_info(char):
    modal True
    # fixed:
    #     xsize 1.0
    #     ysize 1.0
    zorder 3
    
    frame:
        button:
            xalign 0.5
            yalign 0.99
            text "CONFIRM" size 30 style "debug_text"
            hover_background Solid("#5080FF")
            background Solid("#808080")
            action Hide("sce_char_editor_info")
        xalign 0.5
        yalign 0.5
        xsize 0.3
        ysize 0.8
        background Solid("#333")

        if isinstance(char, Character):
            fixed:
                xpos 0.3
                add char.img.idle
                fixed:
                    xpos 58
                    add char.img.big

            text "name:" style "classicfont" xalign 0.1 ypos 75
            button:
                xalign 0.5 ypos 70
                hover_background Solid("#5080FF")
                text char.name font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
                action Call("label_edit_info",char,"name")
            text "item:" style "classicfont" xalign 0.1 ypos 120
            button:
                xalign 0.5 ypos 120
                hover_background Solid("#5080FF")
                action Call("label_edit_info",char,"inventory")
                if len(char.inventory) > 0:
                    text str(char.inventory[0]) font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
                else:
                    text "-" font "IREADCASLON.TTF" size 30 color "#eee" antialias False xalign
            
            for i, field in enumerate( [["vision:","vision"],["movement:","move"],["strong? (can push\nsofas better)","isStrong"],["blind?","isBlind"]] ):
                fixed:
                    ypos 170+60*i
                    text field[0] style "classicfont" xalign 0.1 
                    button:
                        xalign 0.5
                        hover_background Solid("#5080FF")
                        text str(char.stat[field[1]]) font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
                        action Call("label_edit_info",char,field[1])

                
        elif isinstance(char, Slasher):
            fixed:
                xpos 0.3
                add char.img.idle
                fixed:
                    xpos 58
                    add char.img.big
            text "name:" style "classicfont" xalign 0.1 ypos 75
            button:
                xalign 0.5 ypos 70
                hover_background Solid("#5080FF")
                text char.name font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
                action Call("label_edit_info",char,"name")
            text "can open doors:" style "classicfont" xalign 0.1 ypos 120
            button:
                xalign 0.5 ypos 120
                hover_background Solid("#5080FF")
                action Call("label_edit_info",char,"canOpenDoors")
                if char.canOpenDoors:
                    text "YES" font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
                else:
                    text "NO" font "IREADCASLON.TTF" size 30 color "#eee" antialias False 

            text "movement:" style "classicfont" xalign 0.1 ypos 220
            button:
                xalign 0.5 ypos 220
                hover_background Solid("#5080FF")
                action Call("label_edit_info",char,"move")
                text str(char.stat["move"]) font "IREADCASLON.TTF" size 30 color "#eee" antialias False 
        