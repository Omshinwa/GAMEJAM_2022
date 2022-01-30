###########################################################
#                SQUARE
init offset = -1
init python:
    class Square:
        def __init__(self, x, y, type = 1, visibility = 0):
            tile = Tiletype(type)
            self.x = x
            self.y = y
            self.xpos = x * settings["tilesize"]
            self.ypos = y * settings["tilesize"]
            self.isStand = tile.isStand #can we stand on it or not?
            self.visibility = visibility
            self.img = {}
            self.img.idle = tile.idle
            self.img.hover = "img_cell_hover"
            self.img.unstand = "game-UI/cell-unstand.png"
            self.empty = 1 - self.isStand #0 theres nothing there

        def __repr__(self):
            return " x" +str(self.x)+ ":y" +str(self.y)+" "

        def sprite(self):
            # getMouseId()
            # if store.mousexid == self.x and store.mouseyid == self.y:
            #     img = self.img.hover

            if self.isStand == 1:
                if game.state == "moving" and self in game.premoving_where:
                    img = self.img.hover
                else:
                    img = self.img.idle
            else:
                img = self.img.unstand
            return img
