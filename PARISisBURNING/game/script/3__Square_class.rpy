###########################################################
#                SQUARE
init offset = -1
init python:
    class Square(Tiletype):
        def __init__(self, x, y, type, filename):
            super(Square,self).__init__(type)
            self.type = type
            self.x = x
            self.y = y
            self.xpos = x * settings["tilesize"]
            self.ypos = y * settings["tilesize"]
            self.img_hover = "img_cell_hover"
            self.onAction = []

            #make the tile black
            self.isHidden = 0

            self.onFire = 0
            if type == 51:
                self.onFire = 1

            try:
                self.isStand
            except:
                print("ERROR TYPE "+ self.type)
            else:
                self.occupied = 1 - self.isStand #0 theres nothing there

            try:
                settings["event"][ chr(ord('@')+y+1) + str(x) ]
            except:
                self.event = False
            else:
                thisEvent = settings["event"][ chr(ord('@')+y+1) + str(x) ]
                if "variables" in thisEvent:
                    self.event = Event_Caller(name=chr(ord('@')+y+1) + str(x), range=0, isActive=False, label="lab_" + filename + "_" + chr(ord('@')+y+1) + str(x) , variables=thisEvent["variables"])
                else:
                    self.event = Event_Caller(name=chr(ord('@')+y+1) + str(x), range=0, isActive=False, label="lab_" + filename + "_" + chr(ord('@')+y+1) + str(x) )

            if Tiletype.addInteraction(self.itemType):
                self.onAction.append( Tiletype.addInteraction( self.itemType ) )

        def __repr__(self):
            return " x" +str(self.x)+ ":y" +str(self.y)+" "

        def sprite(self):
            return self.img_idle
