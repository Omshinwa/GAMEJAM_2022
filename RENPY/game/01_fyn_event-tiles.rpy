init offset = -2
init python:
    settings["events_fyn"] = { "D2" : {"label":"lab_D2", "variables":1},
    "H8": {"label":"lab_H8"}}

    settings["doors"] = {"B09B10":0, "D16E16": 0, "J03J04": 0, "J06K06":1}
    settings["walls"] = ["J05K05", "J07K07"]


label lab_D2(variables):
    if variables>0:
        "Hello world"
        $ settings["events_fyn"]["D2"]["variables"] = 0
    jump lab_gameloop

label lab_H8:
    "Hello world2"
    jump lab_gameloop

label lab_passTurn(teen):
    python:
        game.premoving_who = ""
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
        if game.totalAP() <= 0:
            game.turnChange()
        game.state = "waiting"
        if game.totalAP() <= 0:
            game.turnChange()

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
