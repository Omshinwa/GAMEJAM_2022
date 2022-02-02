#INITIALIZE THE BOARD
label lab_tile_editor_logic:
python:
    game = Game()
    debug_ = Debug()
    game.maxY =  settings["mapsize"][1]
    game.maxX = settings["mapsize"][0]
    for y in range( game.maxY+1 ):
        game.grid.append([]) #add first row
        for x in range( game.maxX+1 ):
            try:
                settings["tilemap"][y][x]
            except IndexError:
                game.grid[y].append( Square(x=x, y=y, type = "error" ) )
            else:
                game.grid[y].append( Square(x=x, y=y, type = settings["tilemap"][y][x] ) )
            game.gridlist.append( game.grid[y][x] )
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
        if debug_.draw_layer == "tile":
            debug_.draw_on_tile( debug_.tilebrush )
        elif debug_.draw_layer == "wall":
            debug_.draw_on_intersection( what = 1 )
        elif debug_.draw_layer == "closed_door":
            debug_.draw_on_intersection( what = 2 )
        elif debug_.draw_layer == "open_door":
            debug_.draw_on_intersection( what = 3 )
jump lab_tile_editor_render

label label_choose_tile_brush:
    python:
        debug_.choose_tile_brush()
        debug_.draw_layer = "tile"
jump lab_tile_editor_render
