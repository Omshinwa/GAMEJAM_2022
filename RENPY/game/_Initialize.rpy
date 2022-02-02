###############################################################################**
#### INITIALIZE THE GAME BOARD
#################################################################################
label lab_initialize:
python:
    settings["events"] = merge_two_dicts( settings["events_fyn"], settings["events_madi"])

    game = Game()
    game.maxY =  settings["mapsize"][1]
    game.maxX = settings["mapsize"][0]
    for y in range( game.maxY+1 ):
        game.grid.append([]) #add first row
        for x in range( game.maxX+1 ):
            try:
                settings["tilemap"][y][x]
            except IndexError:
                game.grid[y].append( Square(x=x, y=y, type = 0 ) )
            else:
                game.grid[y].append( Square(x=x, y=y, type = settings["tilemap"][y][x] ) )
            game.gridlist.append( game.grid[y][x] )

    # game.grid_getCol = lambda x: [element for element in game.gridlist if element.y == x ]  # list of all elements with .n==30

    def gride(y,x):
        return game.grid[y][x]

    lauren = Character( name = "lauren", x = 2, y = 6)
    game.teens.append( lauren )
    william = Character( name = "william", x = 17, y = 8)
    game.teens.append( william )
    darryl = Character( name = "darryl", x = 15, y = 4)
    game.teens.append( darryl )
    kayleigh = Character( name = "kayleigh", x = 5, y = 8)
    game.teens.append( kayleigh )

    game.state = "waiting"
    slasher = Slasher(name="Slasher", x=12, y=12)
    game.dooms.append( slasher )

    slasher2 = Slasher(name="Slasher", x=10, y=11)
    game.dooms.append( slasher2 )
    game.updateVision()
return


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

    call lab_render from _call_lab_render
    return

label lab_turnChange(): # WAITING (event) > DOOM > FIRE WHENEVER WE WANT TO CHANGE PHASE
    python:
        game.updateVision()

        if game.state == "event":
            game.state = "waiting"

        if game.state == "waiting" and game.totalAP() > 0:
            renpy.jump("lab_gameloop")

        elif game.state == "waiting" and game.totalAP() <= 0:
            game.state = "doom"
            for doom in game.dooms:
                doom.move()
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
                    for direction in [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]:
                        if case.y+direction[1]>=0 and case.x+direction[0]>=0 and case.y+direction[1]<game.maxY and case.x+direction[0]<game.maxX:
                            neighbor = gridcopy[case.y+direction[1]][case.x+direction[0]]

                            if game.isCrossable(case.x, case.y, neighbor.x, neighbor.y, ifdoom = False, ifwalls=True, ifstoppable=False, ifdoors=False):
                                fireScore += neighbor.onFire

                    if fireScore >= settings["fireThreshold"] + 4:
                        game.grid[case.y][case.x].onFire = 2
                        game.grid[case.y][case.x].isStand = 0
                        game.grid[case.y][case.x].itemType = None
                    elif fireScore >= settings["fireThreshold"] and game.grid[case.y][case.x].occupied==0:
                        game.grid[case.y][case.x].onFire = 1
                        game.grid[case.y][case.x].itemType = "little_flame"


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
                renpy.call("lab_kill",teen)

        renpy.jump("lab_turnChange")

label lab_kill(teen):
    python:
        teen.isAlive = 0
        game.grid[teen.y][teen.x].occupied = 0
        renpy.jump("lab_turnChange")

label lab_gameover:
    "lolgg"
    "score: [game.score]"
    return

label lab_doommove_random(self): #this is random
    python:
        for doom in game.dooms:
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
                        i = self.stat.move #end the for loop
                    else:
                        randomInd += 1
                        randomDir = direction[ randomInd%4 ]

                doom.x = doom.x + randomDir[0]
                doom.y = doom.y + randomDir[1]
                renpy.pause(0.1)
                game.grid[doom.y][doom.x].occupied = "doom"
                for teen in game.teens:
                    if doom.x == teen.x and doom.y == teen.y:
                        teen.isAlive = 0
                        game.grid[teen.y][teen.x].occupied = 0
    jump lab_turnChange

label lab_doommove_track(self):
    python:
        for doom in game.dooms:
            target = [99,""]
            cible = ""
            for teen in game.teens:
                if teen.isAlive:
                    distance = distBetween(doom, teen, game, 20)
                    print("cible:"+teen.name+" distance:" + str(distance[0]))
                    if target[0] > distance[0]:
                        target = distance
                        cible = teen
                        print("target:"+str(target[0]))

            # if target[0] == 99:
            #     for teen in game.teens:
            #         if teen.isAlive:
            #             distance = distBetween(doom, teen, game, 5, False)
            #             print("cible:"+teen.name+" distance:" + str(distance[0]))
            #             print("target:"+str(target[0]))
            #             if target[0] > distance[0]:
            #                 target = distance
            #                 cible = teen

            if target[0] == 99: ##HERE ITS THE SAME AS RANDOMWALK
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
                            i = self.stat.move #end the for loop
                        else:
                            randomInd += 1
                            randomDir = direction[ randomInd%4 ]

                    doom.x = doom.x + randomDir[0]
                    doom.y = doom.y + randomDir[1]
                    if game.grid[doom.y][doom.x].type==20:
                        renpy.music.play("audio/step4.wav", channel='sound')
                    else:
                        renpy.music.play("audio/step4.wav", channel='sound')
                    renpy.pause(0.5)
                    game.grid[doom.y][doom.x].occupied = "doom"
                    for teen in game.teens:
                        if doom.x == teen.x and doom.y == teen.y:
                            renpy.call(lab_kill,teen)
                renpy.jump("lab_turnChange")

            for i in range(doom.stat.move):
                print(i)
                game.grid[doom.y][doom.x].occupied = 0

                if i < len(target[1]):
                    if game.isCrossable(target[1][len(target[1]) - 1 - i].x,target[1][len(target[1]) - 1 - i].y, doom.x,doom.y):
                        doom.x = target[1][len(target[1]) - 1 - i].x
                        doom.y = target[1][len(target[1]) - 1 - i].y

                        sound_walk(doom)
                    else:
                        i = doom.stat.move

                game.grid[doom.y][doom.x].occupied = "doom"

                for teen in game.teens:
                    if doom.x == teen.x and doom.y == teen.y:
                        teen.isAlive = 0
                        game.grid[teen.y][teen.x].occupied = 0
    jump lab_turnChange
