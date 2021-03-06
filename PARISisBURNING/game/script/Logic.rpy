###############################################################################**
#### BUNCHES OF LABELS
#################################################################################

label lab_gameloop: #when you just wait for user to do something
    if not game.state == "select":
        $ game.updateVision()

    call lab_check_gameover

    if game.state == "waiting" and game.totalAP() <= 0:
        jump lab_turnChange

    # jump lab_render
    call screen sce_gameloop
    jump lab_gameloop

label lab_end_turn():
    python:
        for teen in game.teens:
            teen.AP = 0
        renpy.jump("lab_gameloop")

label lab_turnChange(): # WAITING (event) > DOOM > FIRE WHENEVER WE WANT TO CHANGE PHASE
    $ game.updateVision()
        # renpy.jump("lab_fireSpread")

    call lab_check_gameover


    if game.state == "event":
        $ game.state = "waiting"

    if game.state == "waiting" and game.totalAP() > 0:
        $ renpy.jump("lab_gameloop")

    elif game.state == "waiting" and game.totalAP() <= 0:
        $ game.state = "doom"
        $ game.doommove()
        $ renpy.jump("lab_turnChange")

    elif game.state == "doom":
        $ game.state = "fire"
        $ renpy.jump("lab_fireSpread")
        $ renpy.jump("lab_turnChange")

    elif game.state == "fire":
        $ game.score += 1
        $ Character.restore_totalAP()
        $ game.state = "event"
        $ i = 0
        while i < len(game.after_every_action):
            python:
                for key in game.after_every_action[i]:
                    square_name = key
            $ renpy.call( "lab_"+game.filename+"_auto_"+square_name, teen, game.grid[teen.y][teen.x], i)
            $ i+=1
        $ game.state = "waiting"
        $ renpy.jump("lab_turnChange")

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
                        # for direction in [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]: si on utilise ??a, il faut modifier isCrossable pour que ??a prenne en compte les diagonales comme updatevision
                            if Game.isValid( x= case.x+direction[0],y= case.y+direction[1] ):
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

label lab_check_gameover:
    # if sum(teen.isAlive == 1 for teen in game.teens) <=0:
    #     "lolgg"
    #     "score: [game.score]"
    #     $ MainMenu(confirm=False)()
    $ renpy.call("lab_"+ game.filename +"_check_gameover")
    return