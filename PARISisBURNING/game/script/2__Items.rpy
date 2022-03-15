##########SET UP THE BOARD###############
init offset = -2
init python:

    class Event_Caller(): #ADDED INSIDE SQUARES. DEFINE HOW ACTIONS ARE ADDED
        def __init__(self, name, range, isActive, text=None, label=None, variables=None):
            self.name = name
            self.range = range
            self.text = text  #only matter if it's an action
            self.label = label
            self.variables = variables
            self.isActive = isActive #if it's not Active, then it's passive
            self.isPassive = not isActive

        def add_action(self, game, teen, case, distance):
            if self.text is not None and distance <= self.range:
                if self.range == 0:
                    i = (teen, case, self.variables)
                    game.actions.append( { "text": self.text, "label": self.label, "variables": i} )

                if self.range == 1:
                    i = (teen, case, self.variables)
                    direction = case.x-teen.x, case.y-teen.y
                    if direction == (0,-1):
                        direction = "up"
                    elif direction == (0,1):
                        direction = "down"
                    elif direction == (-1,0):
                        direction = "left"
                    elif direction == (1,0):
                        direction = "right"
                    print direction
                    game.actions.append( { "text": self.text + " "+ direction, "label": self.label, "variables": i })     
        
        def add_event(self,teen,case):
            renpy.call( self.label, (teen, case, self.variables) )
        
        def __str__(self):
            return "Event_Caller obj '"+self.name+"'"

    def Items(name=""):
        if len(name.split(" "))>1:
            args = name.split(" ")[1]
            name = name.split(" ")[0]
        else:
            args = None

        if name == "Bucket":
            return Item_Bucket(args)
        elif name =='':
            return
        else:
            raise Exception('Item type doesnt exist: '+name)

    class Item_Bucket(): #Event_Caller
        def __init__(self, charge):
            if charge == None:
                charge = 0
            self.name = "Bucket"
            self.charge = int(charge)
            self.maxcharge = 3
            self.args = int(charge)

        def __str__(self):
            return self.name + " "+ str(self.charge)

        def add_action(self, game, teen):
            if game.grid[teen.y][teen.x].itemType == "Shower" or game.grid[teen.y][teen.x].itemType == "Toilet":
                if self.charge < self.maxcharge:
                    game.actions.append( { "text": "Fill the bucket", "label": "lab_fill_bucket", "variables": (self,teen) })

            if self.charge >= 1:
                game.actions.append( { "text": "Throw water", "label": "lab_throw_water", "variables": (self,teen) })
            
            # game.actions.append( { "text": "Discard Bucket", "label": "lab_discard", "variables": (self,teen) } )
