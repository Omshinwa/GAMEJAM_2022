label start:
    show screen keybinds
    jump lab_gameloop
    return

label lab_gameloop:
    python:
        game.updateVision()
        if sum(teen.isAlive == 1 for teen in game.teens) <=0:
            renpy.jump("lab_gameover")
        if game.state == "event":
            game.state = "waiting"
        if game.totalAP() <= 0:
            game.turnChange()

    call lab_render from _call_lab_render
    return

label lab_gameover:
    "lolgg"
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
    jump lab_gameloop

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

            if target[0] == 99:
                for teen in game.teens:
                    if teen.isAlive:
                        distance = distBetween(doom, teen, game, 5, False)
                        print("cible:"+teen.name+" distance:" + str(distance[0]))
                        print("target:"+str(target[0]))
                        if target[0] > distance[0]:
                            target = distance
                            cible = teen

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
                            teen.isAlive = 0
                            game.grid[teen.y][teen.x].occupied = 0
                renpy.jump("lab_gameloop")

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
    jump lab_gameloop
