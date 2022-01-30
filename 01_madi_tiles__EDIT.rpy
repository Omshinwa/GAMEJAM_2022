init offset = -2

##AJOUTE DES DIFFERENTS TILES ICI, CHANGE IDLE POUR CHANGER LE LOOK DU TILE
init python:
    class Tiletype:
        def __init__(self, type):
            self.img = {}

            if type == 0: #CANT STAND ON IT
                self.isStand = 1 #can we stand on that?
                self.img.idle = "game-UI/0.gif"
                self.blockVision = 1

            if type == 1:
                self.isStand = 1
                self.img.idle = "game-UI/1.gif"
                self.blockVision = 0

            if type == 2:
                self.isStand = 1
                self.img.idle = "game-UI/2.gif"
                self.blockVision = 0

            if type == 3:
                self.isStand = 1
                self.img.idle = "game-UI/3.gif"
                self.blockVision = 0

            if type == 4:
                self.isStand = 1
                self.img.idle = "game-UI/4.gif"
                self.blockVision = 0

            if type == 5:
                self.isStand = 1
                self.img.idle = "game-UI/5.gif"
                self.blockVision = 0

            if type == 6:
                self.isStand = 0
                self.img.idle = "game-UI/6.gif"
                self.blockVision = 0

            if type == 7:
                self.isStand = 1
                self.img.idle = "game-UI/7.gif"
                self.blockVision = 0

            if type == 8:
                self.isStand = 1
                self.img.idle = "game-UI/8.gif"
                self.blockVision = 0

            if type == 9:
                self.isStand = 1
                self.img.idle = "game-UI/9.gif"
                self.blockVision = 0

            if type == 11:
                self.isStand = 1
                self.img.idle = "game-UI/11.gif"
                self.blockVision = 0

            if type == 12:
                self.isStand = 1
                self.img.idle = "game-UI/12.gif"
                self.blockVision = 0

            if type == 13:
                self.isStand = 1
                self.img.idle = "game-UI/13.gif"
                self.blockVision = 0

            if type == 14:
                self.isStand = 1
                self.img.idle = "game-UI/14.gif"
                self.blockVision = 0

            if type == 15:
                self.isStand = 1
                self.img.idle = "game-UI/15.gif"
                self.blockVision = 0

            if type == 16:
                self.isStand = 1
                self.img.idle = "game-UI/16.gif"
                self.blockVision = 0

            if type == 17:
                self.isStand = 1
                self.img.idle = "game-UI/17.gif"
                self.blockVision = 0

##CETTE MAP DETERMINE LA TILE
    settings["tilemap"] = [
[ 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 9, 6, 6, 6, 11, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 8, 8, 8, 6, 6, 6, 6, 1, 1, 0, 0, 0, 0, 0, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 16, 8, 14, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 6, 6, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 6, 6, 8, 6, 8, 8, 6, 6, 3, 3, 6, 2, 2, 2, 3, 15, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 6, 6, 8, 6, 6, 6, 6, 6, 3, 3, 6, 2, 2, 2, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 6, 6, 8, 6, 6, 6, 4, 4, 4, 6, 6, 2, 2, 2, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 6, 6, 8, 6, 0, 6, 4, 4, 4, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 8, 6, 8, 3, 3, 6, 0, 6, 6, 1, 1, 6, 6, 6, 1, 6, 6, 6, 2, 13, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 5, 5, 5, 6, 2, 2, 2, 6, 6, 6, 1, 1, 6, 6, 6, 1, 6, 6, 6, 2, 12, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 10, 6, 6, 2, 2, 2, 6, 6, 5, 5, 5, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 6, 6, 6, 6, 0, 0, 6, 6, 5, 5, 5, 8, 8, 0, 0, 0, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 6, 6, 6, 6, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 2, 12, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
[ 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],]

##CETTE MAP DETERMINE LA SALLE (tous les nombres avec 1 représente la salle 1)
    settings["room"] = [
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]
