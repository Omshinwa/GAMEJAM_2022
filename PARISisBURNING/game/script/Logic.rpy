###############################################################################**
#### BUNCHES OF LABELS
#################################################################################

label lab_gameloop: #when you just wait for user to do something
    python:
        if not game.state == "pre_action":
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
        # renpy.jump("lab_fireSpread")

        if sum(teen.isAlive == 1 for teen in game.teens) <=0:
            renpy.jump("lab_gameover")

        if game.state == "event":
            game.state = "waiting"

        if game.state == "waiting" and game.totalAP() > 0:
            renpy.jump("lab_gameloop")

        elif game.state == "waiting" and game.totalAP() <= 0:
            game.state = "doom"
            game.doommove()
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
        if game.score%2 == 0:
            gridcopy = copy.deepcopy(game.grid)
            for copyrow in gridcopy:
                for case in copyrow:

                    realcase = game.grid[case.y][case.x]
                    if case.onFire <=0 :

                        fireScore = 0
                        if case.onFire == -1: #if theres water
                            fireScore = -3
                        elif case.onFire == -2: #if theres blood
                            fireScore = -3

                        for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                        # for direction in [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]: si on utilise ça, il faut modifier isCrossable pour que ça prenne en compte les diagonales comme updatevision
                            if Game.squareExist( x= case.x+direction[0],y= case.y+direction[1] ):
                                neighbor = gridcopy[case.y+direction[1]][case.x+direction[0]]
                                
                                if neighbor.onFire > 0: #fire spreads, water doesnt:
                                    if game.isCrossable(x2=case.x, y2=case.y, x=neighbor.x, y=neighbor.y, exception_arr=["doom","teen"], ifwall=True, ifdoor=False):
                                        fireScore += neighbor.onFire

                        fireScore = min( int( fireScore / 3 ), 3)

                        if fireScore >= 3:
                            realcase.onFire = 3
                            realcase.occupied = "fire"
                        elif fireScore == 2:
                            realcase.onFire = 2
                            realcase.occupied = "fire"
                        elif fireScore == 1 and realcase.occupied==0:
                            realcase.onFire = 1
                            realcase.itemType = "little_flame"
                        elif fireScore == 0:
                            realcase.onFire = 0

                    else:
                        if case.onFire == 1:
                            realcase.onFire = 2
                            realcase.occupied = "fire"
                            realcase.itemType = None
                        elif case.onFire == 2:
                            realcase.onFire = 3
                            realcase.occupied = "fire"
                            realcase.itemType = None

            renpy.pause(0.2)

        for teen in game.teens:
            if game.grid[teen.y][teen.x].onFire >= 2:
                teen.die()

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