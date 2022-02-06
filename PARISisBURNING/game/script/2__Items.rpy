##########SET UP THE BOARD###############
init offset = -2
init python:

    class Item_Action(): #ADDED INSIDE SQUARES. DEFINE HOW ACTIONS ARE ADDED
        def __init__(self, name, isItem, rangeOfActivation, text=None, label=None,variables=None):
            self.name = name
            self.isItem = isItem
            self.range = rangeOfActivation
            self.text = text
            self.label = label
            self.variables = variables
        
        def __repr__(self):
            return "item_Action obj '"+self.name+"'"
        
        
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
                    game.actions.append( { "text": self.text + " "+ direction, "label": self.label, "variables": i })


    class Bucket(Item_Action):
        def __init__(self):
            # super(Bucket,self).__init__( name="Bucket", isItem=True, rangeOfActivation=0)
            self.name = "Bucket"
            self.charge = 0
            self.isItem = True
        
        def add_action(self, game, teen):
            if game.grid[teen.y][teen.x].itemType == "Shower" or game.grid[teen.y][teen.x].itemType == "Toilet":
                game.actions.append( { "text": "Fill the bucket", "label": "lab_fill_bucket", "variables": (self,teen) })

            if self.charge >= 1:
                game.actions.append( { "text": "Throw water", "label": "lab_throw_water", "variables": (self,teen) })
            
            game.actions.append( { "text": "Discard Bucket", "label": "lab_discard", "variables": (self,teen) } )