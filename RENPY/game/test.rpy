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
        smile = Image("smile.png")

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

    hide repulsor

    # Clean up.
    python:
        del repulsor
        del repulsor_sprites
        del repulsor_pos





init python:

    import math

    class Appearing(renpy.Displayable):

        def __init__(self, child, opaque_distance, transparent_distance, **kwargs):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(Appearing, self).__init__(**kwargs)

            # The child.
            self.child = renpy.displayable(child)

            # The distance at which the child will become fully opaque, and
            # where it will become fully transparent. The former must be less
            # than the latter.
            self.opaque_distance = opaque_distance
            self.transparent_distance = transparent_distance

            # The alpha channel of the child.
            self.alpha = 0.0

            # The width and height of us, and our child.
            self.width = 0
            self.height = 0

        def render(self, width, height, st, at):

            # Create a transform, that can adjust the alpha channel of the
            # child.
            t = Transform(child=self.child, alpha=self.alpha)

            # Create a render from the child.
            child_render = renpy.render(t, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = child_render.get_size()

            # Create the render we will return.
            render = renpy.Render(self.width, self.height)

            # Blit (draw) the child's render to our render.
            render.blit(child_render, (0, 0))

            # Return the render.
            return render

        def event(self, ev, x, y, st):

            # Compute the distance between the center of this displayable and
            # the mouse pointer. The mouse pointer is supplied in x and y,
            # relative to the upper-left corner of the displayable.
            distance = math.hypot(x - (self.width / 2), y - (self.height / 2))

            # Base on the distance, figure out an alpha.
            if distance <= self.opaque_distance:
                alpha = 1.0
            elif distance >= self.transparent_distance:
                alpha = 0.0
            else:
                alpha = 1.0 - 1.0 * (distance - self.opaque_distance) / (self.transparent_distance - self.opaque_distance)

            # If the alpha has changed, trigger a redraw event.
            if alpha != self.alpha:
                self.alpha = alpha
                renpy.redraw(self, 0)

            # Pass the event to our child.
            return self.child.event(ev, x, y, st)

        def visit(self):
            return [ self.child ]

screen alpha_magic:
    add Appearing("smile.png", 100, 200):
        xalign 0.5
        yalign 0.5
