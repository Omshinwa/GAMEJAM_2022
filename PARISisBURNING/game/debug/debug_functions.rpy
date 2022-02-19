init offset = -3
init python:
################################################################################
    ##THESE FUNCTIONS CAN BE USED ANYWHERE
################################################################################

    def gridAZ(game, x):
        return game.grid[ ord(x[0])-65 ][int(x[1])]

    #search size = final distance - 1 if there's no obstacle
    def distBetween(start, destination, search_size, **kwargs):
        class Cell:
            def __init__(self,start,destination,gcost, state = "???", parent=""):
                self.x = start.x
                self.y = start.y
                self.gcost = gcost
                self.hcost = abs(start.x - destination.x) + abs(start.y - destination.y)
                self.fcost = self.gcost + self.hcost
                self.state = state
                self.parent = parent
            def __repr__(self):
                return " x" +str(self.x)+ ":y" +str(self.y)+" "

        def trouve_enfant(x, array):
            if x != "":
                array.append(x)
                trouve_enfant(x.parent, array)
            return array
        cells = {}
        cells[start.x,start.y] = Cell(start,destination,0, "open")

        array = {}
        for key, value in cells.iteritems():
            if cells[key].state == "open":
                array[key] = cells[key]

        for notusedvariablelol in range(search_size):
            array = {}
            for key, value in cells.iteritems():
                if cells[key].state == "open":
                    array[key] = cells[key]

            min = 999
            currentArray = []
            for key, value in array.iteritems():
                if array[key].fcost < min:
                    currentArray = [ array[key] ]
                    min = array[key].fcost
                if array[key].fcost == min:
                    currentArray.append( array[key] )

            min = 999
            for k in currentArray:
                if k.hcost < min:
                    current = k

            current.state = "closed"

            if (current.x,current.y) == (destination.x, destination.y):
                array = []
                array = trouve_enfant(current.parent, array)

                if len(array)>0:
                    array.insert(0, destination )
                    del array[-1]

                return [current.fcost, list(reversed(array))]

            for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                pos = {}
                pos.x = current.x + direction[0]
                pos.y = current.y + direction[1]

                if not (pos.x,pos.y) in cells:
                    neighbor = Cell( pos, destination, current.gcost+1, "???",current)
                else:
                    neighbor = Cell( pos, destination, current.gcost+1, cells[pos.x,pos.y].state,current) #is current the dad?


                if (not game.isCrossable( x2=neighbor.x, y2=neighbor.y, x=current.x, y=current.y, **kwargs ) ) or neighbor.state == "closed":
                    pass

                else:
                    if neighbor.state != "open" or neighbor.fcost < cells[neighbor.x,neighbor.y].fcost:
                        cells[pos.x,pos.y] = neighbor
                        if neighbor.state != "open":
                            cells[pos.x,pos.y] = neighbor
                            cells[pos.x,pos.y].state = "open"

        return [999,""]

    def debugmode():
        game.debug_mode = 1 - game.debug_mode
        for row in game.grid:
            for cell in row:
                cell.visibility = 1

    def AZto09(key):
        x = int(key[1:3])
        y = ord(key[0])-65
        if len(key)>3:
            x2 = int(key[4:6])
            y2 = ord(key[3])-65
            return x,y,x2,y2
        return x,y

    def _09toAZ(x,y,x2 = None,y2 = None):
        name = ""
        firstpart = ""
        secondpart = ""
        if x<10:
            firstpart = chr(ord('@')+y+1) + "0" + str(x)
        else:
            firstpart = chr(ord('@')+y+1) + str(x)

        if x2 is not None:
            if x2<10:
                secondpart = chr(ord('@')+y2+1) + "0" + str(x2)
            else:
                secondpart = chr(ord('@')+y2+1) + str(x2)

        name = firstpart + secondpart
        return name

    def id2pos(x):
        return int(x * settings["tilesize"])

    def pos2id(x):
        return int(x / settings["tilesize"])

    def getMousePos():
        x, y = renpy.get_mouse_pos()
        return (x,y)

    def getMouseId():
        x, y = renpy.get_mouse_pos()
        return (pos2id(x),pos2id(y))

    def Arr_to_Maptxt(array):
        output = ""
        for row in array:
            for element in row:
                if len(str(element)) == 2:
                    output += str(element)
                if len(str(element)) == 1:
                    output += " "
                    output += str(element)
                output += " "
            output += "\n"
        return output

    def Maptxt_to_Arr(maptxt):
        output = []
        for row in maptxt.split('\n'):
            chunks, chunk_size = len(row), 3
            if chunks > 0:
                stringarray =  [ row[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
                #this array has everything as three characters str ex: " 6 " or " 50"
                correctarray = []
                for element in stringarray:
                    try:
                        int(element)
                    except:
                        correctarray.append( element.strip() )#remove whitespaces
                    else:
                        correctarray.append( int(element) )
                output.append( correctarray )
        return output

    def send_to_file(filename, text):
        with open(config.gamedir + "/" + filename, "w") as f:
            f.write(text)
        return

    def read_file(filename):
        f = open(renpy.loader.transfn( filename ),"r")
        output = ""
        for line in f:
            output += line + "\n"
        return output

    def read_data_tilemap(filename = ".data_tilemap"):
        return Maptxt_to_Arr( read_file(filename) )

    def export_data_tilemap(filename = ".data_tilemap"):
        settings["tilemap"] = []
        for row in game.grid:
            settings["tilemap"].append( [x.type for x in row] )
        send_to_file( filename, Arr_to_Maptxt( settings["tilemap"] ) )

    def TileTypeTxt_to_Arr( tiletxt ):
        output = []
        for row in tiletxt.split('\n'):
            if len(row) > 0:
                if row[0] != "#":
                #type
                    var_type = row[0:3]
                    try:
                        int(var_type)
                    except:
                        var_type = var_type.strip()
                    else:
                        var_type = int(var_type)

                    row = row[3:]
                    row = row.replace('"','')
                    row = row.split(' ')
                    dict_others = {}
                    for i, item in enumerate( row ):
                        if i == 0:
                            var_url = item
                        else:
                            try:
                                int(item.split(":")[1])
                            except:
                                dict_value = item.split(":")[1]
                            else:
                                dict_value = int(item.split(":")[1])
                            dict_others[item.split(":")[0]] = dict_value

                    objecttile = {"type":var_type, "img_idle":var_url, "variables":dict_others}
                    output.append( objecttile )
        return output

    def Arr_to_TileTypeTxt():
        pass

################################################################################
    ##ALL THE METHODES UNDER ARE ONLY SUPPOSED TO BE USED IN DEBUG MODE
################################################################################
    class Debug():
        def __init__(self):
            self.state = ""
            self.tilebrush = -1
            self.draw_mode = "tile"
            self.previous_tile = False
        def draw_on_tile(self, what= -1, where = None):
            print("bite")
            if where is None:
                where = getMouseId()
            game.grid[where[1]][where[0]] = Square(x=where[0], y=where[1], type = what )

        def choose_tile_brush(self, where = None):
            if where is None:
                where = getMouseId()
            try:
                settings["tiletype"][ 6 * where[1] + (where[0]-(settings["mapsize"][0])) ]["type"]
            except:
                pass
            else:
                type_ = settings["tiletype"][ 6 * where[1] + (where[0]-(settings["mapsize"][0])) ]["type"]
                print(type_)
                self.tilebrush = type_

        def draw_on_intersection(self, what = 0, where = None):
            if where is None:
                where = getMouseId()
            if self.previous_tile == False:

                self.previous_tile = _09toAZ(where[0],where[1])

            else:
                seconde_case = _09toAZ(where[0],where[1])

                ilssontacote = False
                    #SONT ILS A COTE?
                if self.previous_tile[0] == seconde_case[0]:
                    if abs(int(self.previous_tile[1:3]) - int(seconde_case[1:3])) == 1:
                        ilssontacote = True
                elif self.previous_tile[1:3] == seconde_case[1:3]:
                    if abs( ord(self.previous_tile[0]) - ord(seconde_case[0]) ) == 1:
                        ilssontacote = True

                if ilssontacote:
                    if self.previous_tile < seconde_case:
                        ligne = self.previous_tile + seconde_case
                    elif self.previous_tile > seconde_case:
                        ligne = seconde_case + self.previous_tile

                    if ligne in settings["lignes"] and settings["lignes"][ligne] == what:
                        del settings["lignes"][ligne]
                    else:
                        settings["lignes"][ligne] = what

                self.previous_tile = False

    def moveEverything(diffx,diffy):
        

        dictbuffer = {}
        for key, value in settings["lignes"].iteritems():

            x1,y1,x2,y2 = AZto09(key)

            x1 += diffx
            y1 += diffy
            x2 += diffx
            y2 += diffy

            if x1>=0 and x2>=0 and x1< settings["mapsize"][0] and x2< settings["mapsize"][0]:
                if y1>=0 and y2>=0 and y1< settings["mapsize"][1] and y2< settings["mapsize"][1]:
                    new_key = _09toAZ(x1,y1,x2,y2)
                    print new_key
                    dictbuffer[new_key] = settings["lignes"][key]
        settings["lignes"] = copy.deepcopy(dictbuffer)

        gamecopy = copy.deepcopy(game.grid)
        for j, row in enumerate(game.grid):
            for i, case in enumerate(row):
                if Game.squareExist(y= j+diffy, x=i+diffx):
                    game.grid[j+diffy][i+diffx] = Square(x=i+diffx, y=j+diffy, type = gamecopy[j][i].type )
