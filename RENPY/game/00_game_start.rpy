init offset = -3
init python:

    def merge_two_dicts(x, y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z

    def isOn(self, x):
        return x in self

    settings = {}

    settings["tilesize"] = 48.0 #in pixel
    settings["resolution"] = (1380.0,816.0)

    import math
    import random
    import pygame
    import copy
    from operator import attrgetter
