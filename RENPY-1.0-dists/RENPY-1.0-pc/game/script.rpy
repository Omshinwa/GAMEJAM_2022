label start:
    show screen keybinds
    jump lab_gameloop
    return

label lab_gameloop:
    python:
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

label lab_doommove(self):
    python:
        for i in range(self.stat.move):
            game.grid[self.y][self.x].occupied = 0
            validMove = False

            while validMove == False:
                direction = [(-1,0),(0,1),(1,0),(0,-1)]
                randomInd = random.randint(0,3)
                randomDir = direction[ randomInd ]
                if game.isCrossable(self.x+randomDir[0],self.y+randomDir[1]):
                    validMove = True
                elif randomInd >= randomInd%4 + 4:
                    validMove = True
                    randomDir = (0,0)
                    i = self.stat.move #end the for loop
                else:
                    randomInd += 1
                    randomDir = direction[ randomInd%4 ]

            self.x = self.x + randomDir[0]
            self.y = self.y + randomDir[1]
            renpy.pause(0.1)
            game.grid[self.y][self.x].occupied = 1
            for teen in game.teens:
                if self.x == teen.x and self.y == teen.y:
                    teen.isAlive = 0
                    game.grid[teen.y][teen.x].occupied = 0
    jump lab_gameloop
