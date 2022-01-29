init python:
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

            if i.x > repulsor.width - 2:
                i.x = repulsor.width - 2

            if i.y < 2:
                i.y = 2

            if i.y > repulsor.height - 2:
                i.y = repulsor.height - 2

        return .01
#update=grid2_update,
    # On an event, record the mouse position.
    def grid2_event(ev, x, y, st):
        store.grid2_pos = (x, y)

    grid2 = SpriteManager(event=grid2_event)
    grid2_sprites = [ ]
    grid2_pos = None

    # Ensure we only have one smile displayable.
    smile = Image("game-UI/cell-idle.png")
    for i in range(len(game.gridlist)):
        grid2_sprites.append(grid2.create(smile))
        grid2_sprites[i].x = id2pos(game.gridlist[i].x)
        grid2_sprites[i].y = id2pos(game.gridlist[i].y)
    # Position the 400 sprites.

    del smile
    del i
