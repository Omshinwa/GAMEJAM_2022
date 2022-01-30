init python:
    import math

    def repulsor_update(st):

        # If we don't know where the mouse is, give up.
        if repulsor_pos is None:
            return .01

        px, py = repulsor_pos

        # For each sprite...
        for i in repulsor_sprites:

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

    # On an event, record the mouse position.
    def repulsor_event(ev, x, y, st):
        store.repulsor_pos = (x, y)


label repulsor_demo:

    python:
        # Create a sprite manager.
        repulsor = SpriteManager(update=repulsor_update, event=repulsor_event)
        repulsor_sprites = [ ]
        repulsor_pos = None

        # Ensure we only have one smile displayable.
        smile = Image("game-UI/cell-idle.png")

        # Add 400 sprites.
        for i in range(400):
            repulsor_sprites.append(repulsor.create(smile))

        # Position the 400 sprites.
        for i in repulsor_sprites:
            i.x = renpy.random.randint(2, 798)
            i.y = renpy.random.randint(2, 598)

        del smile
        del i

    # Add the repulsor to the screen.
    show expression repulsor as repulsor
    "..."
    # hide repulsor
    #
    # # Clean up.
    # python:
    #     del repulsor
    #     del repulsor_sprites
    #     del repulsor_pos

    return
