init offset = -2
init python:
    # CETTE MAP DETERMINE LA TILE
    settings["tilemap"] = [
[50,50,50,50,50,50,50,50,50,50,50,51, 9,50,50,51, 11,50,50,51,51,51,51,51,51,51,51,50,51],
[50, 8, 99, 8,50,50,50,50,92, 1, 0, 0, 0, 0, 0, 4, 4, 4,50,50,50,50,50,50,50,50,50,50,51],
[50, 11, 8, 14,50,50,50,50,50,50,50,50,50,50,50, 4, 4, 97,50,50,50,50,50,50,50,50,51,50,51],
[50,50, 8,50,50,50, 8, 8, 8, 8, 8, 8, 8,50,50, 4, 4, 4,50,50,50,50,50,50,50,50,50,50,50,51],
[ 6, 6, 8, 6, 6, 6, 8, 6, 8, 8, 6, 6, 3, 85, 6, 2, 2, 2, 3, 15, 50,50, 50,50,50,50,51, 51, 51],
[ 6, 6, 8, 6, 6, 6, 8, 6, 6, 6, 6, 6, 3, 87, 6, 2, 2, 2, 3, 3, 50, 50, 50, 50, 50, 50, 50,51,51],
[ 6, 6, 8, 6, 6, 6, 8, 6, 6, 6, 93, 4, 4, 6, 6, 2, 2, 2, 3, 3, 50, 50, 50, 50, 50, 50, 50, 51, 51],
[ 6, 6, 8, 6, 6, 6, 8, 6, 0, 6, 4, 4, 4, 6, 6, 6, 1, 1, 6, 6, 50, 50, 50, 50, 50, 51, 50, 51, 51],
[ 6, 6, 8, 6, 8, 87, 3, 6, 0, 6, 6, 1, 1, 1, 1, 1, 1, 1, 6, 6, 2, 13, 50, 50, 50,50, 51, 51, 51],
[ 6, 89, 5, 5, 1, 1, 1, 1, 1, 200, 200, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 50, 50, 50,51,51,51,51],
[ 6, 96, 5, 5, 6, 2, 2, 2, 6, 6, 6, 1, 1, 6, 6, 6, 1, 1, 6, 6, 2, 12, 50, 50, 50,50,50,51,51, 51],
[ 50, 50, 10, 50, 50, 2, 2, 2, 6, 6, 5, 5, 5, 6, 6, 6, 1, 1, 6, 6, 50, 50, 50, 50, 50,50,51,51,51, 51],
[ 50, 50, 50, 50, 50, 6, 84, 0, 6, 6, 5, 5, 5, 8, 8, 0, 0, 0, 90, 8, 50, 50,50,50, 50,50,50,51,51, 51],
[ 50, 50, 50, 50, 50, 6, 86, 0, 6, 6, 6, 6, 6, 6, 6, 94, 0, 98, 95, 2, 50,50,50, 50,50,50,50, 51,51],
[ 51, 50, 50, 50, 50, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 0, 83, 0, 2, 12, 50, 50,50,50, 50,50,50,51, 51],
[ 51, 51, 50, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51],
[ 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51]]


    class Tiletype:

        def interaction(self, type, distance, teen, case):
            return False
            # if type == "Couch":
            #     if distance == 1:
            #         return { "text": "Move the couch", "label": "lab_moveCouch", "variables":(self,case) }
            # else:
            #     return False

        def __init__(self, type, visibility = 0):
            self.img = {}
            self.blockVision = 0 #default value, hide the vision behind it like a big object
            self.isDark = 0 #always hidden if 1
            self.visibility = visibility
            self.img.idle = "game-UI/cell-blank.png"

            if type == 50: #GRASS
                    self.isStand = 1 #can we stand on that?
                    self.img.idle = "game-UI/grass.png"
                    self.blockVision = 0
                    self.itemType = None

            if type == 51: #FIREGRASS
                    self.isStand = 1 #can we stand on that?
                    self.img.idle = "game-UI/grass.png"
                    self.blockVision = 0
                    self.itemType = None

            if type == 0: #CANT STAND ON IT
                    self.isStand = 1 #can we stand on that?
                    self.img.idle = "game-UI/0.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 2:
                    self.isStand = 1
                    self.img.idle = "game-UI/1.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 1:
                    self.isStand = 1
                    self.img.idle = "game-UI/2.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 3:
                    self.isStand = 1
                    self.img.idle = "game-UI/3.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 4:
                    self.isStand = 1
                    self.img.idle = "game-UI/4.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 5:
                    self.isStand = 1
                    self.img.idle = "game-UI/5.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 6: #THICK WALL
                    self.isStand = 0
                    self.img.idle = "game-UI/6.gif"
                    self.blockVision = 1
                    self.isDark = 0
                    self.itemType = None

            if type == 7:
                    self.isStand = 1
                    self.img.idle = "game-UI/7.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 8:
                    self.isStand = 1
                    self.img.idle = "game-UI/8.gif"
                    self.blockVision = 0
                    self.isDark = 1
                    self.itemType = None

            if type == 9:
                    self.isStand = 0
                    self.img.idle = "game-UI/9.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 10:
                    self.isStand = 0
                    self.img.idle = "game-UI/10.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 11:
                    self.isStand = 0
                    self.img.idle = "game-UI/11.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 12:
                    self.isStand = 0
                    self.img.idle = "game-UI/12.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 13:
                    self.isStand = 0
                    self.img.idle = "game-UI/13.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 14:
                    self.isStand = 0
                    self.img.idle = "game-UI/14.gif"
                    self.blockVision = 1
                    self.itemType = None

            if type == 15:
                    self.isStand = 0
                    self.img.idle = "game-UI/15.gif"
                    self.blockVision = 0
                    self.itemType = None

            if type == 16:
                    self.isStand = 0
                    self.img.idle = "game-UI/16.gif"
                    self.blockVision = 1
                    self.itemType = None

            if type == 17:
                    self.isStand = 0
                    self.img.idle = "game-UI/17.gif"
                    self.blockVision = 0
                    self.itemType = None

        ## Item types are defined underneath

            if type == 99:
                    self.isStand = 0
                    self.img.idle = "game-UI/coffingrey.gif"
                    self.blockVision = 0
                    self.itemType = "Coffin"

            if type == 98:
                    self.isStand = 0
                    self.img.idle = "game-UI/couchgreen.gif"
                    self.blockVision = 0
                    self.itemType = "Couch"

            if type == 97:
                    self.isStand = 0
                    self.img.idle = "game-UI/couchpurple.gif"
                    self.blockVision = 0
                    self.itemType = "Couch"

            if type == 96:
                    self.isStand = 0
                    self.img.idle = "game-UI/deskblue.gif"
                    self.blockVision = 0
                    self.itemType = "Desk"

            if type == 95:
                    self.isStand = 0
                    self.img.idle = "game-UI/deskyellow.gif"
                    self.blockVision = 0
                    self.itemType = "Desk"

            if type == 94:
                    self.isStand = 1
                    self.img.idle = "game-UI/librarygreen2.gif"
                    self.blockVision = 0
                    self.itemType = "Library"

            if type == 83:
                    self.isStand = 1
                    self.img.idle = "game-UI/librarygreen1.gif"
                    self.blockVision = 0
                    self.itemType = "Library"

            if type == 93:
                    self.isStand = 1
                    self.img.idle = "game-UI/librarypurple.gif"
                    self.blockVision = 0
                    self.itemType = "Library"

            if type == 92:
                    self.isStand = 1
                    self.img.idle = "game-UI/photosred.gif"
                    self.blockVision = 0
                    self.itemType = "Photos"

            if type == 91:
                    self.isStand = 1
                    self.img.idle = "game-UI/photosred.gif"
                    self.blockVision = 0
                    self.itemType = "Photos"

            if type == 90:
                    self.isStand = 1
                    self.img.idle = "game-UI/safegrey.gif"
                    self.blockVision = 0
                    self.itemType = "Safe"

            if type == 89:
                    self.isStand = 0
                    self.img.idle = "game-UI/screenblue.gif"
                    self.blockVision = 0
                    self.itemType = "Screen"

            if type == 87:
                    self.isStand = 1
                    self.img.idle = "game-UI/showercyan.gif"
                    self.blockVision = 0
                    self.itemType = "Shower"

            if type == 86:
                    self.isStand = 1
                    self.img.idle = "game-UI/showergreen.gif"
                    self.blockVision = 0
                    self.itemType = "Shower"

            if type == 85:
                    self.isStand = 1
                    self.img.idle = "game-UI/toiletcyan.gif"
                    self.blockVision = 0
                    self.itemType = "Toilet"

            if type == 84:
                    self.isStand = 1
                    self.img.idle = "game-UI/toiletgreen.gif"
                    self.blockVision = 0
                    self.itemType = "Toilet"

            if type == 200:
                    self.isStand = 1
                    self.img.idle = "game-UI/puddle-sd.png"
                    self.blockVision = 0
                    self.itemType = None
#
# #CETTE MAP DETERMINE LA TILE
#     settings["tilemap"] = [
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 14, 14, 14, 1, 14, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [ 1, 1, 1, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]

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
