###############################################################################**
#### BUNCHES OF LABELS
#################################################################################

label lab_gameloop: #when you just wait for user to do something
    python:
        if not game.state == "action":
            game.updateVision()
        if sum(teen.isAlive == 1 for teen in game.teens) <=0:
            renpy.jump("lab_gameover")

        if game.state == "action":
            game.state == "waiting"

        if game.state == "event":
            game.state = "waiting"

        if game.state == "waiting" and game.totalAP() <= 0:
            renpy.jump( "lab_turnChange" )

    jump lab_render

label lab_end_turn():
    python:
        for teen in game.teens:
            teen.AP = 0
        renpy.jump("lab_gameloop")

label lab_turnChange(): # WAITING (event) > DOOM > FIRE WHENEVER WE WANT TO CHANGE PHASE
    python:
        game.updateVision()

        if sum(teen.isAlive == 1 for teen in game.teens) <=0:
            renpy.jump("lab_gameover")

        if game.state == "event":
            game.state = "waiting"

        if game.state == "waiting" and game.totalAP() > 0:
            renpy.jump("lab_gameloop")

        elif game.state == "waiting" and game.totalAP() <= 0:
            game.state = "doom"
            game.doommove()

            # for doom in game.dooms:
            # renpy.call("lab_doommove",doom)
            renpy.jump("lab_turnChange")

        elif game.state == "doom":
            game.state = "fire"
            renpy.jump("lab_fireSpread")
            renpy.jump("lab_turnChange")

        elif game.state == "fire":
            game.score += 1
            game.restore_totalAP()
            game.state = "waiting"
            renpy.jump("lab_turnChange")


label lab_fireSpread():
    python:
        gridcopy = copy.deepcopy(game.grid)
        for idnex in gridcopy:
            for case in idnex:
                if case.onFire <=0 :
                    fireScore = case.onFire

                    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                    # for direction in [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]: si on utilise ça, il faut modifier isCrossable pour que ça prenne en compte les diagonales comme updatevision
                        if case.y+direction[1]>=0 and case.x+direction[0]>=0 and case.y+direction[1]<game.maxY and case.x+direction[0]<game.maxX:
                            neighbor = gridcopy[case.y+direction[1]][case.x+direction[0]]
                            
                            if neighbor.onFire > 0: #fire spreads, water doesnt:
                                if game.isCrossable(x2=case.x, y2=case.y, x=neighbor.x, y=neighbor.y, ifteen=False, ifdoom = False, ifwall=True, ifdoor=False):
                                    fireScore += neighbor.onFire

                    if fireScore >= settings["fireThreshold"]:
                        game.grid[case.y][case.x].onFire = 2
                        game.grid[case.y][case.x].isStand = 0
                        game.grid[case.y][case.x].itemType = None
                    elif fireScore >= settings["fireThreshold"]/2 and game.grid[case.y][case.x].occupied==0:
                        game.grid[case.y][case.x].onFire = 1
                        game.grid[case.y][case.x].itemType = "little_flame"

                    # game.grid[case.y][case.x].onFire = min( int( fireScore / 3 ), 3)


        for idnex in gridcopy:
            for case in idnex:
                realcase = game.grid[case.y][case.x]
                if case.type == 51:
                    realcase.onFire = 3
                    realcase.isStand = 0
                    realcase.itemType = None
                elif case.onFire == 1:
                    realcase.onFire = 2
                    realcase.isStand = 0
                    realcase.itemType = None
                elif case.onFire == 2:
                    realcase.onFire = 3
                    realcase.isStand = 0
                    realcase.itemType = None

        renpy.pause(0.2)

        for teen in game.teens:
            if game.grid[teen.y][teen.x].onFire >= 2:
                game.debug = "105"
                renpy.call("lab_kill", teen)

        renpy.jump("lab_turnChange")

label lab_kill(teen):
    python:
        if teen.isAlive == 1:
            teen.isAlive = 0
            game.grid[teen.y][teen.x].occupied = 0
            if teen.name in ["william","darryl"]: #is that a boi
                renpy.music.play("audio/manstab.ogg", channel='sound')
            else:
                renpy.music.play("audio/girlstab.ogg", channel='sound')
            renpy.pause(0.2)
            renpy.jump("lab_turnChange")
    return

label lab_gameover:
    "lolgg"
    "score: [game.score]"
    return


################################################################################
#######DECISION MAKING: first try if there's anyone near reacheable, then just randomwalk otherwise
label lab_doommove(doom):
    python:

        # for doom in game.dooms:
        target = [99,""]
        cible = ""
        for teen in game.teens:
            if teen.isAlive:
                distance = distBetween(start=doom, destination=teen, search_size=doom.stat.move*20, ifteen=False, ifdoom=False, canOpenDoors=doom.canOpenDoors)
                print("cible:"+teen.name+" distance:" + str(distance[0]))
                if target[0] > distance[0]:
                    target = distance
                    cible = teen

        print("target:"+str(target[1]))
        
    if target[0] == 99: ##HERE ITS THE SAME AS RANDOMWALK
        call lab_doommove_random(doom)
    else:
        call lab_doommove_track(doom, cible, target)
    
    python:
        for teen in game.teens:
            if doom.x == teen.x and doom.y == teen.y:
                teen.die()

    return

label lab_doommove_random(doom):
    python:
        for i in range(doom.stat.move):
            game.grid[doom.y][doom.x].occupied = 0
            validMove = False

            while validMove == False:
                direction = [(-1,0),(0,1),(1,0),(0,-1)]
                randomInd = random.randint(0,3)
                randomDir = direction[ randomInd ]
                if game.isCrossable(doom.x+randomDir[0],doom.y+randomDir[1],doom.x,doom.y):
                    validMove = True
                elif randomInd >= randomInd%4 + 4:
                    validMove = True
                    randomDir = (0,0)
                    i = doom.stat.move #end the for loop
                else:
                    randomInd += 1
                    randomDir = direction[ randomInd%4 ]

            doom.x = doom.x + randomDir[0]
            doom.y = doom.y + randomDir[1]

            doom.sound_walk(doom)

            game.grid[doom.y][doom.x].occupied = "doom"
    return

label lab_doommove_track(doom,cible,target):
    python:
        for i in range( doom.stat.move ):

            if len(target[1]) > i:

                #can he just straight up walk there?
                if game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=doom.x, y=doom.y, ifdoom = False, ifwall=True, ifdoor=True, ifteen=False, lastMovement=(len(target[1]) == 0) ):

                    game.grid[doom.y][doom.x].occupied = 0
                    doom.x = target[1][i].x
                    doom.y = target[1][i].y
                    doom.sound_walk(doom)

                #or is there a door?
                elif doom.canOpenDoors and game.isCrossable(x2= target[1][i].x, y2 = target[1][i].y, x=doom.x, y=doom.y,
                    ifdoom = False, ifwall=True, ifdoor=False, ifteen=False, lastMovement=(len(target[1]) == 0) ):

                        print("theres a door")

                        if action_door(doom.x,doom.y, target[1][i].x,target[1][i].y):
                            game.grid[doom.y][doom.x].occupied = 0
                            doom.x = target[1][i].x
                            doom.y = target[1][i].y
                            doom.sound_walk(doom)
                        else:
                            i = doom.stat.move

                else:
                    i = doom.stat.move

            game.grid[doom.y][doom.x].occupied = "doom"
    return