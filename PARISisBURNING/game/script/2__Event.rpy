###############################"
# DEFINE DOORS, WALLS, AND SQUARE EVENTS

init offset = -2
init python:

    #THOSE ARE PASSIVE EVENTS AND AUTOMATICALLY TRIGGERS
    settings["events_fyn"] = { "D2" : {"label":"lab_D2", "variables":1},
    "H8": {"label":"lab_H8"}, "B8" : {"label":"lab_B8"}}

    settings["actions"] = {}
    settings["lignes"] = json.loads( read_file(".data_lignes") )

##BY DEFAULT VARIABLES[0] is the teen doing the action, VARIABLE[1] is the square, VARIABLE[2] are the other vars passed by the Action
label lab_moveCouch(variable):
    python:
        teen = variable[0]
        sofa = variable[1]
        direction = sofa.x - teen.x, sofa.y - teen.y
        #if the next case is empty
        if game.squareExist(sofa.y + direction[1], sofa.x + direction[0]):
            if game.grid[sofa.y + direction[1]][sofa.x + direction[0]].isStand and game.grid[sofa.y + direction[1]][sofa.x + direction[0]].occupied == 0:
                intermediaire = copy.deepcopy(game.grid[sofa.y][sofa.x])
                game.grid[sofa.y][sofa.x] = copy.deepcopy( game.grid[sofa.y + direction[1]][sofa.x + direction[0]] )
                game.grid[sofa.y + direction[1]][sofa.x + direction[0]] = copy.deepcopy(intermediaire)

                game.grid[sofa.y + direction[1]][sofa.x + direction[0]].x = sofa.x + direction[0]
                game.grid[sofa.y + direction[1]][sofa.x + direction[0]].y = sofa.y + direction[1]
                game.grid[sofa.y][sofa.x].x = sofa.x
                game.grid[sofa.y][sofa.x].y = sofa.y

                renpy.music.play("audio/pushfurniture.wav", channel='sound')
                renpy.pause(0.5)
                
    call lab_passTurn(copy.copy(game.premoving_who))
    return

label lab_action_door(variable): #currently used by teens
    python:
        vari = variable[2]
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
        game.updateVision()
        renpy.pause(0.5)
    call lab_passTurn(copy.copy(game.premoving_who))
    return

init python:
                
    def action_door(x,y,x2,y2): #currently used by slashers

        for action in game.grid[y][x].onAction:
            if action.name == "door":
                vari = action.variables

                a = game.grid[y][x].occupied or game.grid[y][x].isStand == 0
                b = game.grid[y2][x2].occupied or game.grid[y2][x2].isStand == 0
                print("door action:")
                print(a)
                print(b)
                print(settings["lignes"][vari])
                if a and b:
                    renpy.music.play("audio/doorfail.ogg", channel='sound')
                    return False
                else:
                    if settings["lignes"][vari]== 2:
                        renpy.music.play("audio/opendoor1.mp3", channel='sound')
                        renpy.pause(0.5)
                        settings["lignes"][vari] = 3
                    elif settings["lignes"][vari]== 3:
                        renpy.music.play("audio/closedoor1.wav", channel='sound')
                        renpy.pause(0.5)
                        settings["lignes"][vari] = 2
                    return True

        return False

label lab_D2(variables):
    if variables>0:
        "Hello world"
        $ settings["events_fyn"]["D2"]["variables"] = 0
    jump lab_gameloop

label lab_B8():
    "Vous rallumez les fusibles"
    python:
        for row in game.grid:
            for cell in row:
                if cell.isDark:
                    cell.isDark = 0
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
    return
    # jump lab_gameloop

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
