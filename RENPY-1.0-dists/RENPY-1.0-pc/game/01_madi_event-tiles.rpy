init offset = -2
init python:
    settings["events_madi"] = {"E3": "label_E3", "H8": "label_H8"}
    settings["switches_madi"] = {"label_H8_bite": 0}

######################################################################
#EVERY LABEL MUST ENDS WITH JUMP LAB GAMELOOP TO CONTINUE THE GAME
#
#   if you write a python line, you write $ just before
#   ex:        $ bite = "bite"
#   or you put a "python:" statement
######################################################################

label label_E3():
    if not "label_E3" in settings["switches"]: #this is so the label is only run once, you can do that or set your own switches name
        "Hello world madi"
        $ settings["switches_madi"]["label_E3"] = 1
    jump lab_gameloop

label label_H8:
    if settings["switches_madi"]["label_H8_bite"] == 0:
        "Hello world2 madi"
        $ settings["switches_madi"]["label_H8_bite"] = 1
    jump lab_gameloop
