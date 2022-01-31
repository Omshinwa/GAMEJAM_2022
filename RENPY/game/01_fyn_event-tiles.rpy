init offset = -2
init python:
    settings["events_fyn"] = { "D2" : {"label":"lab_D2", "variables":1},
    "H8": {"label":"lab_H8"}, "B8" : {"label":"lab_B8"}}

    settings["actions"] = {}

    settings["doors"] = {"B09B10":0, "D17E17": 1, "J03J04": 1,"B14B15":1, "G17G18":1, "H11I11":1, "F12G12":1, "L17M17":1, "O17O18":1,
    "C02D02":1, "I06J06":0, "J21J22":0, "J05K05":0}

    for key, value in settings["doors"].iteritems():
        x = int(key[1:3])
        y = key[0]
        x2 = int(key[4:6])
        y2 = key[3]
        settings["actions"][y+str(x)]= {"text":"DOOR", "label": "lab_action_door", "variables":key}
        settings["actions"][y2+str(x2)]= {"text":"DOOR", "label": "lab_action_door", "variables":key}

    settings["walls"] = ["H20I20", "H21I21", "E17E18","F17F18","D18E18","D15E15","D16E16","I05J05", "H04I04","J06K06","I04I05","H05I05","J07K07","A01B01","C01D01","C03D033","L16M16","A02B02","A03B03","A08B08","A09B09","A10B10","A11B11","A13B13","A14B14","A15B15","A17B17","B00B01",
    "B03B04","B07B08","B17B18","B08C08","B09C09","B10C10","B11C11","B12C12","B13C13","B14C14","C00C01","C03C04","C14C15","C17C18","C06D06","C07D07","C08D08","C09D09","C10D10","C11D11","C12D12","D01D02","D02D03","D05D06","D07E07","D10E10","D11E11","D13E13","D12D13","D14D15","D17D18","E01E02","E02E03","E05E06","E06E07","E07E08","E08F08","E09F09","E09E10","E11E12","E13E14","E14E15","E19E20","F01F02","F02F03","F05F06","F06F07","F11F12","F10G10","F11G11","F13F14","F14F15","F19F20","G01G02","G02G03","G05G06","G06G07","G08H08","G09G10","G12G13","G14G15","G19G20","H01H02","H02H03","H05H06","H06H07","H07H08","H08H09","H09H10","H12H13","H15H16","H17H18","H10I10","I01I02","I02I03","I03I04","I06I07","I07I08","I08I09","I10I11","I19I20","I21I22","I01J01","I03J03","I07J07","I09J09","I10J10","I18J18","I19J19","J00J1","J04K04","J08K08","J09K09","J10K10","J13K13","J14K14","J15K15","J18K18","J19K19","K00K01","K03K04","K04K05","K07K08","K10K11","K12K13","K15K16","K19K20","K21K22","K01L01","K03L03","K10L10","K20L20","K21L21","L04L05","L07L08","L09L10","L12L13","L13M13","L14M14","L15M15","L18M18","L19M19","L15L16","L05M05","M05M06","M07M08","M09M10","M19M20","M10N10","M11N11","M12N12","M13N13","M14N14","N05N06","N07N08","N14N15","N19N20","N08O08","N09O09","N10O10","N11O11","N12O12","N13O13","N14O14","N14N15","N19N20","O06O07","O19O20","O07P07","O08P08","O09P09","O10P10","O11P11","O12P12","O13P13","O14P14","O15P15","O16P16","O17P17","O18P18","O19P19"]

    settings["fireThreshold"] = 6

label lab_moveCouch(variables):
    python:
        teen = variables[0]
        sofa = variables[1]

label lab_action_door(vari):
    python:
        x = int(vari[1:3])
        y = ord(vari[0])-65
        x2 = int(vari[4:6])
        y2 = ord(vari[3])-65
        a = game.grid[y][x].occupied or game.grid[y][x].isStand == 0
        b = game.grid[y2][x2].occupied or game.grid[y2][x2].isStand == 0
        if a and b:
            renpy.music.play("audio/doorfail.ogg", channel='sound')
            pass
        else:
            if settings["doors"][vari]==0:
                renpy.music.play("audio/opendoor1.mp3", channel='sound')
            else:
                renpy.music.play("audio/closedoor1.wav", channel='sound')
            settings["doors"][vari] = 1 - settings["doors"][vari]


    call lab_passTurn(copy.copy(game.premoving_who)) from _call_lab_passTurn

label lab_D2(variables):
    if variables>0:
        "Hello world"
        $ settings["events_fyn"]["D2"]["variables"] = 0
    jump lab_gameloop

label lab_B8():
    "Vous rallumez les fusibles"
    python:
        for i in game.gridlist:
            if i.isDark:
                i.isDark = 0
    jump lab_gameloop

label lab_H8:
    "Hello world2"
    jump lab_gameloop

#################################################
label lab_passTurn(teen): #QUAND ON FINIT SON TOUR
    python:
        if game.grid[teen.y][teen.x].onFire == 1:
            game.grid[teen.y][teen.x].onFire = 0
        game.premoving_who = ""
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
    jump lab_gameloop

label lab_takeitems(var):
    python:
        thief = var[0]
        cadaver = var[1]
        game.premoving_who = ""
        game.state = "waiting"
        game.grid[teen.y][teen.x].onEvent(game)
        if game.totalAP() <= 0:
            game.turnChange()
        game.state = "waiting"
        if game.totalAP() <= 0:
            game.turnChange()
    jump lab_gameloop
