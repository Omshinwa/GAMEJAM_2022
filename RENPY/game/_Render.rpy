style debug_text is text:
    outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
    color "#FFFFFF"

style style_action:
    color "#00FF00"

label lab_render:
    show screen sce_grid
    show screen sce_doom
    show screen sce_char
    show screen sce_fog
    show screen sce_action
    call screen sce_walls


image img_cell_hover:
    "game-UI/cell-hover-01.png"
    pause(0.1)
    "game-UI/cell-hover-02.png"
    pause(0.1)
    "game-UI/cell-hover-03.png"
    pause(0.1)
    "game-UI/cell-hover-04.png"
    pause(0.1)
    "game-UI/cell-hover-05.png"
    pause(0.1)
    repeat

image img_cell_fog:
    "game-UI/cell-fog-01.png"
    pause(2.0)
    "game-UI/cell-fog-04.png"
    pause(2.0)
    repeat

screen sce_gameloop():
    pass

screen sce_char():
    zorder 1
    #First draw the dead people
    for teen in game.teens:
        if teen.isAlive == 0:
            imagebutton:
                xpos id2pos(teen.x)
                ypos id2pos(teen.y)
                idle teen.sprite()
                action NullAction()
                sensitive False

    for teen in game.teens:
        if teen.isAlive == 1:
            imagebutton:
                xpos id2pos(teen.x)
                ypos id2pos(teen.y)
                idle teen.sprite()
                if teen.AP > 0 :
                    hover teen.img.hover
                if renpy.get_screen("say") or game.state == "moving":
                    sensitive False
                else:
                    sensitive True
                action Function(teen.premove)

screen sce_doom():

    zorder 2

    for doom in game.dooms:
        imagebutton:
            xpos id2pos(doom.x)
            ypos id2pos(doom.y)
            idle doom.sprite()
            # hover doom.hover()
            action NullAction()
            sensitive game.grid[doom.y][doom.x].visibility

screen sce_action():
    zorder 3
    if game.state=="action":
        button:
            xysize settings["mapsize"][0] * settings["tilesize"], settings["mapsize"][1] * settings["tilesize"]
            action Function(game.premoving_who.cancelMov) #gros bouton pour annuler
    if game.state == "action":
        for i,act in enumerate(game.actions):
                button:
                    xpos id2pos(game.premoving_who.x)+40
                    ypos id2pos(game.premoving_who.y)-40*(i+1)
                    text act["text"] style "style_action" size 30
                    background Solid( "#000000" )
                    hover_background "#00a"
                    if len(act)==2:
                        action [SetVariable("game.premoving_who.AP", 0),  Call(act["label"])]
                    if len(act)==3:
                        action [SetVariable("game.premoving_who.AP", 0),Call(act["label"],act["variables"])]


screen sce_fog():
    zorder 2
    for cell in game.gridlist:
        frame:
            padding (0,0,0,0)
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            if cell.visibility == 0 and not game.debug_mode and game.state!="debug":
                # background Solid( "#00000080" )
                background "game-UI/cell-fog-01.png"
            else:
                background Solid( "#FF000000" )

            if game.debug_mode:
                text chr(ord('@')+cell.y+1) + str(cell.x) size 30*settings["tilesize"]/96 style "debug_text"
                text str(cell.y) + str(cell.x) size 20*settings["tilesize"]/96 ypos 30 style "debug_text"

#EXAMPLE DE COMPOSITE QUI MARCHE
# return Composite(
#         (96, 96),
#         (0, 0), img,
#         (0, 0), Transform( self.img.unstand , alpha = 0.5  ))

screen sce_grid():
    for cell in game.gridlist:
        frame:
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            background cell.sprite()

        if cell.onFire > 0:
            imagebutton:
                xpos int(cell.x * settings["tilesize"])
                ypos int(cell.y * settings["tilesize"])
                xysize int(settings["tilesize"]), int(settings["tilesize"])
                if cell.visibility == 0:
                    idle "game-UI/cell-blank.png"
                else:
                    if cell.onFire == 1:
                        idle "game-UI/small-fire.png"
                    elif cell.onFire == 2:
                        idle "game-UI/fire.png"
                    elif cell.onFire == 3:
                        idle "game-UI/big-fire.png"


    if game.state=="moving":
        button:
            xysize settings["padding"][0] + settings["tilesize"] * settings["mapsize"][0],settings["padding"][1] + settings["tilesize"] * settings["mapsize"][1]
            action [SetVariable("game.state", "waiting"), SetVariable("game.premoving_where", "")] #gros bouton pour annuler
    for cell in game.premoving_where:
        imagebutton:
            xpos int(cell.x * settings["tilesize"])
            ypos int(cell.y * settings["tilesize"])
            xysize int(settings["tilesize"]), int(settings["tilesize"])
            hover game.premoving_who.img.idle
            idle "game-UI/cell-blank.png"
            action Function(game.premoving_who.move, cell=cell)

    # text game.state size 80 color "#FF0000"
    text "SCORE:"+str(game.score) size 40 color "#FF0000" xalign 1.0

screen sce_walls():
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
