###############################"
# DEFINE DOORS, WALLS, AND SQUARE EVENTS

init offset = -2
init python:

    #THOSE ARE PASSIVE EVENTS AND AUTOMATICALLY TRIGGERS
    settings["event"] = { "D2" : {"variables":1}, "B8" : {}}

    settings["actions"] = {}

##BY DEFAULT VARIABLES[0] is the teen doing the action, VARIABLE[1] is the square (call square.x and square.y), VARIABLE[-1] are the other vars passed by the Action


label lab_moveCouch(variable):
    python:
        game.premoving.who.AP -= 1
        sofa = {}
        teen = variable[0]
        sofa.x = variable[1].x
        sofa.y = variable[1].y
        
        howManySquare = 1
        direction = sofa.x - teen.x, sofa.y - teen.y
        if teen.stat["isStrong"]:
            howManySquare = 3
        for i in range(howManySquare):
            start = game.grid[sofa.y][sofa.x]
            end = game.grid[sofa.y + direction[1]][sofa.x + direction[0]]
            print("--")
            print(start)
            print(end)
            #if the next case is empty
            if game.isCrossable(x=start.x, y=start.y, x2=end.x, y2=end.y, lastMovement=True, exception_arr = ["fire"]):
                #so disgusting lol
                start = game.grid[sofa.y][sofa.x]
                end = game.grid[sofa.y + direction[1]][sofa.x + direction[0]]

                start.onAction = [x for x in start.onAction if x.name != "Couch"] 
                end.onAction.append( Tiletype.addInteraction( "Couch" ) )

                buffer = start.type
                buffer_startAction = copy.deepcopy( start.onAction )
                buffer_endAction = copy.deepcopy( end.onAction )

                game.grid[sofa.y][sofa.x] = Square(x=start.x, y=start.y, type = end.type, filename=game.filename)
                game.grid[sofa.y + direction[1]][sofa.x + direction[0]] = Square(x=end.x, y=end.y, type = buffer, filename=game.filename)

                game.grid[sofa.y][sofa.x].onAction = buffer_startAction
                game.grid[sofa.y + direction[1]][sofa.x + direction[0]].onAction = buffer_endAction

                renpy.play("audio/pushfurniture.wav", channel='sound')
                renpy.pause(0.5)
                sofa.x = end.x
                sofa.y = end.y
                
                
    call lab_endTurn(copy.copy(game.premoving.who))
    return

label lab_action_door(variable): #currently used by teens

    $ teen = variable[0]
    $ vari = variable[-1]

    if game.data_line[vari]== 4: #if it's a hidden door
        python:
            game.say(teen,"finds a secret door",False)
            renpy.music.queue("audio/opendoor1.mp3", channel='sound', relative_volume=0.5)
            game.data_line[vari] = 3
            game.makeSecretHidden(variable[1].x,variable[1].y,1)
            renpy.pause(0.5)
        call lab_endTurn(copy.copy(game.premoving.who))
        return

    #if it's a regular door
    python:
        game.premoving.who.AP -= 1
        x = int(vari[1:3])
        y = ord(vari[0])-65
        x2 = int(vari[4:6])
        y2 = ord(vari[3])-65
        a = game.grid[y][x].occupied or game.grid[y][x].isStand == 0
        b = game.grid[y2][x2].occupied or game.grid[y2][x2].isStand == 0
        if a and b:
            renpy.play("audio/doorfail.ogg", channel='sound', relative_volume=0.5)
            pass
        else:
            if game.data_line[vari]== 2:
                renpy.play("audio/opendoor1.mp3", channel='sound', relative_volume=0.5)
                game.data_line[vari] = 3
            elif game.data_line[vari]== 3:
                renpy.play("audio/closedoor1.wav", channel='sound', relative_volume=0.5)
                game.data_line[vari] = 2
        game.updateVision()
        renpy.pause(0.5)
    call lab_endTurn(copy.copy(game.premoving.who))
    return


#################################################
label lab_endTurn(teen): #EVERYTIME THE TURN ENDS YOU CALL endTurn
    python:
        if teen.AP <= 0:
            if game.grid[teen.y][teen.x].onFire == 1:
                game.grid[teen.y][teen.x].onFire = 0
            game.premoving = {}
            game.state = "waiting"
            #game.grid[teen.y][teen.x].onEvent(game)
            if game.grid[teen.y][teen.x].event:
                game.state = "event"
                # renpy.call( game.grid[teen.y][teen.x].event, teen)
                game.grid[teen.y][teen.x].event.add_event( game,teen,game.grid[teen.y][teen.x] )
        else:
            teen.action()
    return

#################################################
label lab_passTurn(teen): #QUAND ON PASSE SON TOUR
    python:
        game.premoving.who.AP = 0
    # call lab_endTurn(copy.copy(game.premoving.who))
        renpy.call("lab_endTurn",copy.copy(game.premoving.who))
    return

label lab_takeitems(var):
    python:
        thief = var[0]
        cadaver = var[1]
        game.premoving = {}
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
        if game.totalAP() <= 0:
            game.turnChange()
        game.state = "waiting"
        if game.totalAP() <= 0:
            game.turnChange()
    jump lab_gameloop


label lab_throw_water(var):
    python:
        #game.premoving.who.AP -= 1
        game.premoving.hover = "game-UI/puddle.png"
        game.premoving.action = "lab_throw_water_confirm"
        game.premoving.variables = var #self
        game.premoving.where = game.inrange2(var[1].x,var[1].y,1, exception_arr=["fire"], ifoccupied = False)
    return

label lab_throw_water_confirm(cell):
    python:
        # teen =  game.premoving.variables[1]
        # direction = cell.x - teen.x, cell.y - teen.y
        # cell2 = game.grid[cell.y + direction[1]][cell.x + direction[0]]

        # if game.isCrossable(x=cell.x, y=cell.y, x2=cell2.x, y2=cell2.y, exception_arr = ["fire"]):
        #     cells = [cell,cell2]
        # else:
        #     cells = [cell]

        # if game.isCrossable(x=cell.x, y=cell.y, x2=cell2.x, y2=cell2.y, exception_arr = ["fire"]):
        #     cells = [cell,cell2]
        
        game.premoving.who.AP -= 1
        #redondant, car quand on call lab_passTurn, AP devient 0
        teen =  game.premoving.variables[1]
        direction = cell.x - teen.x, cell.y - teen.y
        cell2 = game.grid[cell.y + direction[1]][cell.x + direction[0]]

        cells = []
        for direction in [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]:
            if Game.isValid(x=cell2.x + direction[0], y=cell2.y + direction[1]):
                cell = game.grid[cell2.y + direction[1]][cell2.x + direction[0]]
                cells.append(cell)
        cells.append(cell2)

        item = game.premoving.variables[0] #thats the bucket
        item.charge -= 1
        renpy.play("audio/throw-water.ogg", channel='sound')
        for cel in cells:
            if cel.onFire <= 1:
                cel.onFire = -1
            else:
                cel.onFire -= 3
                
            if cel.onFire <= 1 and cel.occupied=="fire":
                cel.occupied = 0
        renpy.pause(0.5)

    call lab_endTurn(copy.copy(game.premoving.who))
    return

label lab_fill_bucket(var):
    python:
        game.premoving.who.AP -= 1
        item = var[0]
        teen = var[1]
        item.charge = item.maxcharge
        if game.grid[teen.y][teen.x].itemType == "Shower":
            renpy.play("audio/fill-water-from-tap.ogg", channel='sound')
        elif game.grid[teen.y][teen.x].itemType == "Toilet":
            renpy.play("audio/fill-water-from-pool.ogg", channel='sound')
        renpy.pause(0.5)
    call lab_endTurn(copy.copy(game.premoving.who))
    return
    

label lab_000_D2(variables):
    $ teen = variables[0]
    $ vari = variables[-1]
    if vari>0:
        $ game.say(teen, "hello world")
        $ settings["event"]["D2"]["variables"] = 0
    jump lab_gameloop

label lab_000_B8(variables):
    "Vous rallumez les fusibles"
    python:
        for row in game.grid:
            for cell in row:
                if cell.isDark:
                    cell.isDark = 0
    jump lab_gameloop