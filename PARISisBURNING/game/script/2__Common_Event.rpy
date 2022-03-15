###############################"
# DEFINE DOORS, WALLS, AND SQUARE EVENTS

init offset = -2

##BY DEFAULT VARIABLES[0] is the teen doing the action, VARIABLE[1] is the square (call square.x and square.y), VARIABLE[-1] are the other vars passed by the Action

label lab_teen_move(teen):
    $ teen.premove()
    return


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
            elif game.data_line[vari]== 4: #if it's a hidden door
                game.say(teen,"finds a secret door",False)
                renpy.music.queue("audio/opendoor1.mp3", channel='sound', relative_volume=0.5)
                game.data_line[vari] = 3
                game.makeSecretHidden(variable[1].x,variable[1].y,1)
        game.updateVision()
        renpy.pause(0.5)
    call lab_endTurn(teen)
    return


#################################################
label lab_endTurn(teen): #EVERYTIME THE TURN ENDS YOU CALL endTurn
    if teen.AP <= 0:
        python:
            if game.grid[teen.y][teen.x].onFire == 1:
                game.grid[teen.y][teen.x].onFire = 0
            # game.premoving = {}
            game.state = "event"
            square_name = _09toAZ(teen.x, teen.y)
        python:
            try:
                game.events[ square_name ]
            except:
                pass
            else:
                game.state = "event"
                renpy.call( "lab_" + game.filename + "_" + square_name, teen, game.grid[teen.y][teen.x] )
        
        $ i = 0
        while i < len(game.after_every_action):
            python:
                for key in game.after_every_action[i]:
                    square_name = key
            $ renpy.call( "lab_"+game.filename+"_auto_"+square_name, teen, game.grid[teen.y][teen.x], i)
            $ i+=1
        $ game.state = "waiting"
    else:
        $ teen.action()
    return

#################################################
label lab_passTurn(teen): #QUAND ON PASSE SON TOUR
    python:
        game.premoving.who.AP = 0
    # call lab_endTurn(copy.copy(game.premoving.who))
        renpy.call("lab_endTurn",teen)
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
        game.premoving.where = []
        game.premoving.who.AP -= 1
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

    call lab_endTurn(teen)
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
    call lab_endTurn(teen)
    return
    
