init offset = -3
init python:

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
                print("strarr=")
                print(stringarray)
                correctarray = []
                for element in stringarray:
                    try:
                        int(element)
                    except:
                        correctarray.append( element.strip() )#remove whitespaces
                    else:
                        correctarray.append( int(element) )
                print("crtarr=")
                print(correctarray)
                output.append( correctarray )
        return output

    def send_to_file(filename, text):
        with open(config.gamedir + "/" + filename, "w") as f:
            f.write(text)
        return

    def read_file(filename):
        f = open(renpy.loader.transfn( filename ),"r")
        output = ""
        # iterate over its lines and do something with them
        for line in f:
            output += line + "\n"
        # when finished, close the file
        return output

    def read_data_tilemap(filename = ".data_tilemap"):
        return Maptxt_to_Arr( read_file(filename) )

    def export_data_tilemap(filename = ".data_tilemap"):
        send_to_file( filename, Arr_to_Maptxt( settings["tilemap"] ) )
