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
        send_to_file(".data_lignes", json.dumps(settings["lignes"]))
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
jump lab_tile_editor_render

label label_choose_tile_brush:
    python:
        debug_.choose_tile_brush()
        debug_.draw_mode = "tile"
jump lab_tile_editor_render
