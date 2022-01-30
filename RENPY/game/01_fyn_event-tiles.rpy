init offset = -2
init python:
    settings["events_fyn"] = {"E3": "lab_E3", "H8": "lab_H8"}
    settings["switches_fyn"] = {}

label lab_E3():
    if not "E3" in settings["switches_fyn"]:
        "Hello world"
        $ settings["switches_fyn"]["E3"] = 1
    jump lab_gameloop

label lab_H8:
    "Hello world2"
    jump lab_gameloop
