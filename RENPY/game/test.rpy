init python:
    def grid2_update(st):
        if grid2_pos is None:
            return .01
        gridcopy = copy.deepcopy(grid2_sprites)
        px, py = grid2_pos

        for i,cell in enumerate(gridcopy):

            if pos2id(cell.x) ==1 and pos2id(cell.y)==1 :
                print pos2id(px) == pos2id(cell.x) and pos2id(py) == pos2id(cell.y)
            if pos2id(px) == pos2id(cell.x) and pos2id(py) == pos2id(cell.y):
                grid_corresp = game.grid[pos2id(py)][pos2id(px)]
                smile = Image(grid_corresp.sprite())
                grid2_sprites.append(grid2.create(smile))
                grid2_sprites[-1].x = id2pos(grid_corresp.x)
                grid2_sprites[-1].y = id2pos(grid_corresp.y)

                grid2_sprites[i].destroy()

        return .01

    def repulsor_update(st):

        # If we don't know where the mouse is, give up.
        if grid2_pos is None:
            return .01

        px, py = grid2_pos

        # For each sprite...
        for i in grid2_sprites:

            # Compute the vector between it and the mouse.
            vx = i.x - px
            vy = i.y - py

            # Get the vector length, normalize the vector.
            vl = math.hypot(vx, vy)
            if vl >= 150:
                continue

            # Compute the distance to move.
            distance = 3.0 * (150 - vl) / 150

            # Move
            i.x += distance * vx / vl
            i.y += distance * vy / vl

            # Ensure we stay on the screen.
            if i.x < 2:
                i.x = 2

            if i.x > grid2.width - 2:
                i.x = grid2.width - 2

            if i.y < 2:
                i.y = 2

            if i.y > grid2.height - 2:
                i.y = grid2.height - 2

        return .01

#update=grid2_update,
label grid2_demo:
    # On an event, record the mouse position.
    python:
        def grid2_event(ev, x, y, st):
            store.grid2_pos = (x, y)

        grid2 = SpriteManager( update=grid2_update, event=grid2_event)
        grid2_sprites = [ ]
        grid2_pos = None

        for i in range(len(game.gridlist)):
            smile = Image( game.gridlist[i].sprite() )
            grid2_sprites.append(grid2.create(smile))
            grid2_sprites[i].x = id2pos(game.gridlist[i].x)
            grid2_sprites[i].y = id2pos(game.gridlist[i].y)
        # Position the 400 sprites.
    # Add the repulsor to the screen.
        del smile
        del i

    show expression grid2 as grid2
return
