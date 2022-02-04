###########################################################
#                SQUARE
init offset = -1
init python:
    class Square(Tiletype):
        def __init__(self, x, y, type):
            super(Square,self).__init__(type)
            self.type = type
            self.x = x
            self.y = y
            self.xpos = x * settings["tilesize"]
            self.ypos = y * settings["tilesize"]
            self.img_hover = "img_cell_hover"
            # self.img_unstand = "game-UI/cell-unstand.png"

            self.onFire = 0;
            try:
                self.isStand
            except:
                print("ERROR TYPE "+ self.type)
            else:
                self.occupied = 1 - self.isStand #0 theres nothing there

            try:
                settings["events"][ chr(ord('@')+y+1) + str(x) ]
            except:
                self.event = ""
            else:
                self.event = settings["events"][ chr(ord('@')+y+1) + str(x) ] #str(ord(y)-65

        def __repr__(self):
            return " x" +str(self.x)+ ":y" +str(self.y)+" "

        def sprite(self):
            if game.premoving_where != "":
                if game.state == "moving" and self in game.premoving_where:
                    img = self.img_hover
                else:
                    # if self.type == 50 or self.type == 51:
                    #     if self.visibility:
                    #         return "game-UI/grass.png"
                    #     else:
                    #         return "game-UI/6.gif"
                    img = self.img_idle
            else:
                # if self.type == 50 or self.type == 51:
                #     if self.visibility:
                #         return "game-UI/grass.png"
                #     else:
                #         return "game-UI/6.gif"
                img = self.img_idle

            return img

        def onEvent(self, game):
            if self.event != "":
                game.state = "event"
                if len(self.event) == 1:
                    renpy.call( self.event["label"] )
                else:
                    renpy.call( self.event["label"], self.event["variables"])
