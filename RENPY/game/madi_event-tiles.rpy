init offset = -2
init python:
    settings["events"] = {"E3": "lab_E3", "H8": "lab_H8"}

label lab_E3:
    "Hello world"
    jump lab_gameloop

label lab_H8:
    "Hello world2"
    jump lab_gameloop
