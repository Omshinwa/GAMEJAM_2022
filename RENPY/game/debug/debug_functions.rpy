init offset = -3
init python:
################################################################################
    ##THESE FUNCTIONS CAN BE USED ANYWHERE
################################################################################
    def A_to_0(key):
        x = int(key[1:3])
        y = ord(key[0])-65
        x2 = int(key[4:6])
        y2 = ord(key[3])-65
        return x,y,x2,y2

    def id2pos(x):
        return int(x * settings["tilesize"])

    def pos2id(x):
        return int(x / settings["tilesize"])

    def getMousePos():
        x, y = pygame.mouse.get_pos()
        return (x,y)

    def getMouseId():
        x, y = pygame.mouse.get_pos()
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

    # def py_read_file(filename):
    #     f = open("resources/missions.txt", "r")
    #     f.read()
    #     output = ""
    #     for line in f:
    #         output += line + "\n"
    #     f.close()
    #     return output

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
            self.draw_layer = "tile"
            self.previous_tile = False
        def draw_on_tile(self, what= -1, where = None):
            if where is None:
                where = getMouseId()
            game.grid[where[1]][where[0]] = Square(x=where[0], y=where[1], type = what )

        def choose_tile_brush(self, where = None):
            if where is None:
                where = getMouseId()
            try:
                settings["tiletype"][ 5 * where[1] + (where[0]-(settings["mapsize"][0] + 1)) ]["type"]
            except:
                pass
            else:
                type_ = settings["tiletype"][ 5 * where[1] + (where[0]-(settings["mapsize"][0] + 1)) ]["type"]
                print(type_)
                self.tilebrush = type_

        def draw_on_intersection(self, what = 0, where = None):
            if where is None:
                where = getMouseId()
            if self.previous_tile == False:
                if where[0] < 10:
                    self.previous_tile = chr(ord('@')+where[1]+1) + "0" + str(where[0])
                else:
                    self.previous_tile = chr(ord('@')+where[1]+1) + str(where[0])
            else:
                if where[0] < 10:
                    seconde_case = chr(ord('@')+where[1]+1) + "0" + str(where[0])
                else:
                    seconde_case = chr(ord('@')+where[1]+1) + str(where[0])

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
