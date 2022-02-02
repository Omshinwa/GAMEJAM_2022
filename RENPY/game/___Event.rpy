###############################"
# DEFINE DOORS, WALLS, AND SQUARE EVENTS

init offset = -2
init python:
    settings["events_fyn"] = { "D2" : {"label":"lab_D2", "variables":1},
    "H8": {"label":"lab_H8"}, "B8" : {"label":"lab_B8"}}

    settings["actions"] = {}
    settings["lignes"] = json.loads( read_file(".data_lignes") )

    for key, value in settings["lignes"].iteritems():
        if value == 2 or value == 3:
            x = int(key[1:3])
            y = key[0]
            x2 = int(key[4:6])
            y2 = key[3]
            settings["actions"][y+str(x)]= {"text":"DOOR", "label": "lab_action_door", "variables":key}
            settings["actions"][y2+str(x2)]= {"text":"DOOR", "label": "lab_action_door", "variables":key}

    settings["fireThreshold"] = 6

label lab_moveCouch(variables):
    python:
        teen = variables[0]
        sofa = variables[1]

label lab_action_door(vari):
    python:
        x = int(vari[1:3])
        y = ord(vari[0])-65
        x2 = int(vari[4:6])
        y2 = ord(vari[3])-65
        a = game.grid[y][x].occupied or game.grid[y][x].isStand == 0
        b = game.grid[y2][x2].occupied or game.grid[y2][x2].isStand == 0
        if a and b:
            renpy.music.play("audio/doorfail.ogg", channel='sound')
            pass
        else:
            if settings["lignes"][vari]== 2:
                renpy.music.play("audio/opendoor1.mp3", channel='sound')
                settings["lignes"][vari] = 3
            elif settings["lignes"][vari]== 3:
                renpy.music.play("audio/closedoor1.wav", channel='sound')
                settings["lignes"][vari] = 2


    call lab_passTurn(copy.copy(game.premoving_who)) from _call_lab_passTurn

label lab_D2(variables):
    if variables>0:
        "Hello world"
        $ settings["events_fyn"]["D2"]["variables"] = 0
    jump lab_gameloop

label lab_B8():
    "Vous rallumez les fusibles"
    python:
        for i in game.gridlist:
            if i.isDark:
                i.isDark = 0
    jump lab_gameloop

label lab_H8:
    "Hello world2"
    jump lab_gameloop

#################################################
label lab_passTurn(teen): #QUAND ON FINIT SON TOUR
    python:
        if game.grid[teen.y][teen.x].onFire == 1:
            game.grid[teen.y][teen.x].onFire = 0
        game.premoving_who = ""
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
    jump lab_gameloop

label lab_takeitems(var):
    python:
        thief = var[0]
        cadaver = var[1]
        game.premoving_who = ""
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
        if game.totalAP() <= 0:
            game.turnChange()
        game.state = "waiting"
        if game.totalAP() <= 0:
            game.turnChange()
    jump lab_gameloop
