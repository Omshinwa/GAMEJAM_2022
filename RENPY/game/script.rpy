label start:
    show screen keybinds
    jump lab_gameloop
    return

label lab_gameloop:
    python:
        if game.totalAP() <= 0:
            game.turnChange()
    call lab_render
    return
