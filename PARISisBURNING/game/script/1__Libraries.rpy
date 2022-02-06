init offset = -3
init python:

    def merge_two_dicts(x, y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z

    settings = {}

    settings["tilesize"] = 48 #in pixel, must be integer
    settings["mapsize"] = (25,17)
    settings["padding"] = (0,0)
    settings["fireThreshold"] = 6

    import math
    import random
    import copy
    import json
    import time

    from operator import attrgetter
