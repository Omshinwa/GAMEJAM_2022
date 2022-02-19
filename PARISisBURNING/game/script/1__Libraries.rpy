init offset = -3
init python:

    def merge_two_dicts(x, y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z

    settings = {}
    
    settings["tilesize"] = 48 #in pixel, must be integer
    settings["mapsize"] = (25,17)
    settings["ui-size"] = 7
    settings["resolution"] = ((settings["mapsize"][0]+settings["ui-size"])*settings["tilesize"], settings["mapsize"][1]*settings["tilesize"])
    settings["padding"] = (0,0)
    settings["fireThreshold"] = [3, 6, 9]
    #values of water / lil fire / fire / bigfire

    import math
    import random
    import copy
    import json
    import time

    from operator import attrgetter
