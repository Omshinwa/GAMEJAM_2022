#INITIALIZE THE BOARD
label start2:
label lab_tile_editor_logic:
python:
    game = Game()
    debug_ = Debug()
    game.state = "debug"
jump lab_tile_editor_render

label label_export_tilemap:
    python:
        export_data_tilemap(".data_tilemap")
        send_to_file(".data_lignes", json.dumps({"line":settings["lignes"], "char":settings["char"], "event":settings["events"]}))
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

label label_edit_info(teen, what):
    python:
        if what == "name":
            input_ = renpy.input("", length=14)
            teen.name = input_
        elif what == "inventory":
            input_ = renpy.input("", length=14)
            teen.inventory = [Items(input_)]
        elif what == "vis":
            input_ = renpy.input("", length=2)
            teen.stat.vis = int(input_)
        elif what == "move":
            input_ = renpy.input("", length=1)
            teen.stat.move = int(input_)
    return

