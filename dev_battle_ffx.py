import os
import cv2

# Developer Mode: 0 = off, 1 = on
DEV_MODE = 0

# Battle Mode: 0 = not in Battle, 1 = in Battle
BATTLE_MODE = 0

# Farm Mode: 0 = not Farm, 1 = Farm
FARM_MODE = 1

# Datasets images
BATTLEEND_DATASET = 217.158927976724
TIDUS_DATASET = 424.3147416717925
YUNA_DATASET = 5998.489643235203
KIMAHRI_DATASET = 7991.936498746722
RIKKU_DATASET = 6136.851554339571
AURON_DATASET = 7006.361823371671
LULU_DATASET = 8496.029425561095
WAKKA_DATASET = 6193.9526152530425

# GCV Data Offsets
BATTLEEND_OFFSET = 0
BATTLESTART_OFFSET = 8
FARM_OFFSET = 9
TIDUS_OFFSET = 1
YUNA_OFFSET = 2
KIMAHRI_OFFSET = 3
RIKKU_OFFSET = 4
AURON_OFFSET = 5
LULU_OFFSET = 6
WAKKA_OFFSET = 7



class GCVWorker:
    def __init__(self, width, height):
        os.chdir(os.path.dirname(__file__))
        self.gcvdata = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        #self.gcvdata = bytearray()
        #self.gcvdata.extend(int(value).to_bytes(2, byteorder='big', signed=True))
        self.devon = True
        self.devoff = False
        self.battleon = True
        self.battleoff = False
        self.farmon = True
        self.farmoff = False
        self.char = cv2.imread('img/titus.jpg') # tidus
        self.battleend = cv2.imread('img/battleend.jpg')
        self.foundBattleEnd = True
        self.battle = False
        self.farm = True
        self.found01 = True # tidus
        self.found02 = True # yuna
        self.found03 = True  # kimahri
        self.found04 = True  # rikku
        self.found05 = True  # auron
        self.found06 = True  # lulu
        self.found07 = True  # lulu

    def __del__(self):
        del self.gcvdata
        del self.devon
        del self.devoff
        del self.battleon
        del self.battleoff
        del self.char
        del self.battleend
        del self.battle

    def process(self, frame):
        global DEV_MODE
        global TIDUS_DATASET
        global YUNA_DATASET
        global KIMAHRI_DATASET
        global RIKKU_DATASET
        global AURON_DATASET
        global LULU_DATASET
        global WAKKA_DATASET
        global BATTLEEND_DATASET
        global BATTLEEND_OFFSET
        global BATTLESTART_OFFSET
        global BATTLE_MODE
        global FARM_MODE
        global FARM_OFFSET
        global TIDUS_OFFSET
        global YUNA_OFFSET
        global KIMAHRI_OFFSET
        global RIKKU_OFFSET
        global AURON_OFFSET
        global LULU_OFFSET
        global WAKKA_OFFSET

        self.gcvdata[BATTLEEND_OFFSET] = False
        self.gcvdata[BATTLESTART_OFFSET] = False
        self.gcvdata[FARM_OFFSET] = False
        self.gcvdata[TIDUS_OFFSET] = False
        self.gcvdata[YUNA_OFFSET] = False
        self.gcvdata[KIMAHRI_OFFSET] = False
        self.gcvdata[RIKKU_OFFSET] = False
        self.gcvdata[AURON_OFFSET] = False
        self.gcvdata[LULU_OFFSET] = False
        self.gcvdata[WAKKA_OFFSET] = False

        picturechar = frame[186:219, 1326:1381]
        picturebattleend = frame[764:873, 1326:1381]

        similarchar = cv2.norm(self.char, picturechar)
        similarbattleend = cv2.norm(self.battleend, picturebattleend)

        if DEV_MODE == 0:
            cv2.putText(frame, "DEV MODE: " + str(self.devoff), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
        else:
            cv2.putText(frame, "DEV MODE: " + str(self.devon), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        if BATTLE_MODE == 1:
            self.battle = True

        if BATTLE_MODE == 0:
            self.battle = False

        if FARM_MODE == 1:
            self.farm = True

        if FARM_MODE == 0:
            self.farm = False

        if self.battle == True:
            cv2.putText(frame, "In Battle Mode: " + str(self.battleon), (5, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            self.gcvdata[BATTLESTART_OFFSET] = True

        if self.battle == False:
            cv2.putText(frame, "In Battle Mode: " + str(self.battleoff), (5, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            self.gcvdata[BATTLESTART_OFFSET] = False

        if self.farm == True:
            cv2.putText(frame, "In Farm Mode: " + str(self.farmon), (5, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            self.gcvdata[FARM_OFFSET] = True

        if self.farm == False:
            cv2.putText(frame, "In Farm Mode: " + str(self.farmoff), (5, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            self.gcvdata[FARM_OFFSET] = False

        if similarchar == TIDUS_DATASET and self.found01: # tidus
            print('Found: Tidus')
            self.found01 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[TIDUS_OFFSET] = True
            else:
                self.gcvdata[TIDUS_OFFSET] = False

        elif similarchar == YUNA_DATASET and self.found02: # yuna
            print('Found: Yuna')
            self.found02 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[YUNA_OFFSET] = True
            else:
                self.gcvdata[YUNA_OFFSET] = False

        elif similarchar == KIMAHRI_DATASET and self.found03: # kimahri
            print('Found: Kimahri')
            self.found03 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[KIMAHRI_OFFSET] = True
            else:
                self.gcvdata[KIMAHRI_OFFSET] = False

        elif similarchar == RIKKU_DATASET and self.found04: # rikku
            print('Found: Rikku')
            self.found04 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[RIKKU_OFFSET] = True
            else:
                self.gcvdata[RIKKU_OFFSET] = False

        elif similarchar == AURON_DATASET and self.found05: # auron
            print('Found: Auron')
            self.found05 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[AURON_OFFSET] = True
            else:
                self.gcvdata[AURON_OFFSET] = False

        elif similarchar == LULU_DATASET and self.found06: # lulu
            print('Found: Lulu')
            self.found06 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[LULU_OFFSET] = True
            else:
                self.gcvdata[LULU_OFFSET] = False

        elif similarchar == WAKKA_DATASET and self.found07: # wakka
            print('Found: Wakka')
            self.found07 = False
            BATTLE_MODE = 1
            FARM_MODE = 0
            if DEV_MODE == 0:
                self.gcvdata[WAKKA_OFFSET] = True
            else:
                self.gcvdata[WAKKA_OFFSET] = False

        elif similarchar == TIDUS_DATASET: # tidus
            pass

        elif similarchar == YUNA_DATASET: # yuna
            pass

        elif similarchar == KIMAHRI_DATASET: # kimahri
            pass

        elif similarchar == RIKKU_DATASET: # rikku
            pass

        elif similarchar == AURON_DATASET: # auron
            pass

        elif similarchar == LULU_DATASET: # lulu
            pass

        elif similarchar == WAKKA_DATASET: # wakka
            pass

        else:
            self.found01 = True
            self.found02 = True
            self.found03 = True
            self.found04 = True
            self.found05 = True
            self.found06 = True
            self.found07 = True
            #if DEV_MODE == 1:
                #print(similarchar)

        if similarbattleend == BATTLEEND_DATASET and self.foundBattleEnd:
            print('Found: Battle End')
            self.foundBattleEnd = False
            BATTLE_MODE = 0
            FARM_MODE = 1
            if DEV_MODE == 0:
                self.gcvdata[BATTLEEND_OFFSET] = True
            else:
                self.gcvdata[BATTLEEND_OFFSET] = False

        elif similarbattleend == BATTLEEND_DATASET: # battle end
            pass

        else:
            self.foundBattleEnd = True
            #print(similarbattleend)

        return frame, self.gcvdata
