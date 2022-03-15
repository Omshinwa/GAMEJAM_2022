##BY DEFAULT VARIABLES[0] is the teen doing the action, VARIABLE[1] is the square (call square.x and square.y), VARIABLE[-1] is the ID of the current event

label lab_000_start:
    python:
        global settings
        #THOSE ARE PASSIVE EVENTS AND AUTOMATICALLY TRIGGERS
        game.events = { "B08": 0, "I19":0 }
        game.after_every_action = [ {"00": 0} ] #, {"01":0}
        #NOTE THE DIFFERENCE IN DATA STRUCT

        for teen in game.teens:
            if teen.name == "Tanglei":
                tanglei = teen
            elif teen.name == "William":
                william = teen

        game.updateVision()
        game.state = "event"
        if True:
            game.say("tv", ".....")
            game.say(william, "what's up with the tv?")
            game.say(tanglei, "I don't know, it's been like that since an hour ago.")
            renpy.pause(0.2)
            game.doommove()
            renpy.pause(0.2)
            game.say(tanglei, "hey, did you hear something")
            game.say(william, "hm? it's probably the dog")
            game.say(tanglei, "I think I heard a door opening...")
            game.say(tanglei, "could you go check?")
            game.say(william, "...alright")

        tanglei.maxAP = 0
        tanglei.AP = 0
    return

label lab_000_auto_00(teen, square, id):
    if game.dooms[0].sprite() != "empty.png":
        if game.dooms[0].closest_teen()[0].name == "William":
            python:
                game.say(william, "W-What the hell is that?")
                game.say(game.dooms[0], "Hello, hahahaha")
                game.say(william, "TANGLEI! RUN!")
                game.say(tanglei, "Hein?")
        elif game.dooms[0].closest_teen()[0].name == "Tanglei":
            python:
                game.say(tanglei, "AAAAAAH WHAT'S THAT", speed=8)
                game.say(game.dooms[0], "Hello, hahahaha")
                game.say(william, "TANGLEI! RUN!")
        python:
            renpy.pause(0.2)
            game.say("tv", "OBJECTIVE: exit the house, both players must survive", color="#22b4ee")
            tanglei.maxAP = 2
            tanglei.AP = 2
            del game.after_every_action[ id ]
    return

label lab_000_auto_01(teen, square, id):
    $ game.say("tv","AP:" + str(teen.AP))
    return

label lab_000_I19(teen, square):
    $ game.events["I19"] += 1
    if teen.name == "William":
        $ game.say(william, "Fiou, I'm safe")
        $ game.teens.remove(william)
        $ game.say(william, "escaped", speak=False)
        $ square.occupied = 0
    elif teen.name == "Tanglei":
        $ game.say(tanglei, "*huff* *huff* am I safe now?")
        $ game.say(tanglei, "escaped", speak=False)
        $ game.teens.remove(tanglei)
        $ square.occupied = 0
    if game.events["I19"] == 2:
        $ game.say("william", "Tanglei are you alright?")
        $ game.say("tanglei", "Yea, but what was that?!")
        $ game.say("tv","gg you won, you should save now, im gonna load map 2")
        $ game.say("tv","click when youre ready")
        pause
        call load("001")
    return

# label lab_000_G06(teen, square):
#     $ game.say(teen, "hello world")
#     $ del game.events["G06"]
#     return

label lab_000_B08(teen, square):
    "Vous rallumez les fusibles"
    python:
        for row in game.grid:
            for cell in row:
                if cell.isDark:
                    cell.isDark = 0
    jump lab_gameloop

label lab_000_check_gameover:
    if william.isAlive==0:
        $ game.say(tanglei, "NOOOO WILLIAM!!!")
        "game over"
        $ MainMenu(confirm=False)()
    if tanglei.isAlive==0:
        $ game.say(william, "Tanglei? y-you can still move right?")
        "game over"
        $ MainMenu(confirm=False)()
    return

############################################################################################################"
############################################################################################################"
############################################################################################################"
############################################################################################################"
############################################################################################################"
############################################################################################################"

label lab_001_check_gameover:
    if sum(teen.isAlive == 1 for teen in game.teens) <=0:
        "lolgg"
        "score: [game.score]"
        $ MainMenu(confirm=False)()
    return

label lab_001_start:
    python:
        #THOSE ARE PASSIVE EVENTS AND AUTOMATICALLY TRIGGERS
        game.events = {}
        game.after_every_action = [ {"wincheck": 0} ]

        game.say("tv", "OBJECTIVE: extinguish the fires, use the Bucket objects you have", color="#22b4ee")
        game.say("tv", "the buckets need to be filled with water in toilets and showers first.", color="#22b4ee")
        game.say("tv", "you can close doors and use Sofas to block the doors!", color="#22b4ee")
    return

label lab_001_auto_wincheck(teen, square, id):
    python:
        for row in game.grid:
            for square in row:
                if square.onFire > 0:
                    game.say(teen, "there's still fire on the square "+ str(square.x) + " " + str(square.y), speed=15)
                    renpy.return_statement()
    "wow t'as éteint tous les feux!"
    "gg"
    $ MainMenu(confirm=False)()


label lab_002_check_gameover:
    if sum(teen.isAlive == 1 for teen in game.teens) <=0:
        "lolgg"
        "score: [game.score]"
        $ MainMenu(confirm=False)()
    return

label lab_002_start:
    python:
        #THOSE ARE PASSIVE EVENTS AND AUTOMATICALLY TRIGGERS
        game.events = {}
        game.after_every_action = [ {"wincheck": 0} ]
    return

label lab_002_auto_wincheck(teen, square, id):
    python:
        for row in game.grid:
            for square in row:
                if square.onFire > 0:
                    game.say(teen, "there's still fire on the square "+ str(square.x) + " " + str(square.y), speed=15)
                    renpy.return_statement()
    "wow t'as éteint tous les feux!"
    "gg"
    $ MainMenu(confirm=False)()

