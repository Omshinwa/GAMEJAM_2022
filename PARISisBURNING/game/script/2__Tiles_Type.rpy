init offset = -2
init python:

    class Tiletype:

        def __init__(self, type):
            global settings

            #DEFAULT VALUES
            
            self.type = -1
            self.img_idle = "game-UI/tile-error.png"
            self.isStand = 1
            self.blockVision = 0 #default value, hide the vision behind it like a big object
            self.isDark = 0 #makes people no see anything in it
            self.isSecret = 0 #makes the tile straight up dark, like the tile 6
            self.itemType = None
            self.visibility = 1

            ##THE DEFAULT TILE DOESNT BLOCK VISION, CAN BE STANDED ON

            tiletype = settings["tiletype"]
            for Thistype in tiletype:
                if type == Thistype["type"]:
                    self.img_idle = Thistype["img_idle"]
                    for keys in Thistype["variables"]:
                        setattr(self,keys, Thistype["variables"][keys] )
                    break

        itemTypes = {}
        itemTypes["Couch"] = Event_Caller( name="Couch", text="Push Sofa", isActive=True, label="lab_moveCouch", range=1 )

        @classmethod
        def addInteraction(cls, itemType):
            if itemType in cls.itemTypes:
                return cls.itemTypes[itemType]
            else:
                return False