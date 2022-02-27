#INITIALIZE THE BOARD
label start2:
label lab_tile_editor_logic:
python:
    game = Game("000")
    debug_ = Debug("000")
    game.state = "debug"
jump lab_tile_editor_render

label label_export_tilemap:
    python:
        export_data_tilemap(debug_.filename + "-map.dat")
        send_to_file(debug_.filename + ".dat", json.dumps(get_data_map()))

    'data has been exported'
    jump lab_tile_editor_render

label label_draw_on_tile:
    python:
        if debug_.draw_mode == "tile":
            debug_.draw_on_tile( debug_.tilebrush )
        elif debug_.draw_mode == "wall":
            debug_.draw_on_intersection( what = 1 )
        elif debug_.draw_mode == "closed_door":
            debug_.draw_on_intersection( what = 2 )
        elif debug_.draw_mode == "open_door":
            debug_.draw_on_intersection( what = 3 )
        elif debug_.draw_mode == "hidden_door":
            debug_.draw_on_intersection( what = 4 )

        elif debug_.draw_layer == "char":
                debug_.draw_on_tile( debug_.tilebrush )

jump lab_tile_editor_render

label label_choose_tile_brush:
    python:
        if debug_.draw_layer == "map":
            debug_.draw_mode = "tile"
        elif debug_.draw_layer == "char":
            debug_.draw_mode = "add"
        debug_.choose_tile_brush()
jump lab_tile_editor_render

label label_edit_info(char, what):
    python:
        if what == "name":
            input_ = renpy.input("", length=14)
            char.name = input_
        elif what == "inventory":
            input_ = renpy.input("", length=14)
            if len(input_)>0:
                char.inventory = [Items(input_)]
            else:
                char.inventory = []

        elif what == "vision":
            input_ = renpy.input("", length=2)
            char.stat["vision"] = int(input_)
        elif what == "move":
            input_ = renpy.input("", length=1)
            char.stat["move"] = int(input_)

        else:
            # setattr(char, what, not getattr(char, what) ) #SET ATTRIBUTE BY NAME
            char.stat[what] = not char.stat[what]
    return

