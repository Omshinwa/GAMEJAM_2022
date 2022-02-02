init offset = -3
init python:

    def merge_two_dicts(x, y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z

    def isOn(self, x):
        return x in self

    settings = {}

    settings["tilesize"] = 48 #in pixel, must be integer
    settings["mapsize"] = (27,17)
    settings["padding"] = (0,0)

    import math
    import random
    import pygame
    import copy
    import json
    from operator import attrgetter
