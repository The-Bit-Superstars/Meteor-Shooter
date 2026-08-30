"""
menus:
0: game
1: mainmenu
2: shop
3: helps
4: about
5: mainmenu2 (settings)
6: langselect
7: networkMenu
8: keyboard
9: online #reserved
10: minigame
11: listNetworks
12: langSelectOnStartup
13: skins

skins:
default:   683d5113-3ee2-41bd-96eb-8532b19acc6b
french:    4df7f35e-1f99-46b0-ab23-098a273e3f92
croatia:   a59c3e34-5264-48b5-9daf-15dd051a14fa
bus:       232f7bc2-5264-4aef-977a-d3f3c7a0658e
b2 spirit: d4f134ac-0ce7-43cf-b5fc-4d4b4ac3560c
school 1:  5c5bbe41-fffe-44cd-a44e-ae47f8f05bfe
school 2:  ecb90661-85f0-4263-8726-aa6795a2653e
"""

version = "1.7.0"
# DEVEX znači DEVeloper EXchange
version_type = 'RELEASE'
version_type = version_type.upper()

import network, gc, machine
gc.collect()
wlan = network.WLAN(network.STA_IF)
gc.collect()
wlan.active(True)
from Bit import *
up_button, down_button, left_button, right_button, a_button, b_button, menu_button = Buttons.Up, Buttons.Down, Buttons.Left, Buttons.Right, Buttons.A, Buttons.B, Buttons.C
from framebuf import *
from random import randrange
import math, random, array, time
begin()
from sprite_data import *
skin = 0
sprite_coin = FrameBuffer(coinSprite[3], coinSprite[0], coinSprite[1], RGB565)
meteor_type = [0,0,0]
sprite_asteroid = [FrameBuffer(asteroidTypeSprite[meteor_type[0]][0], 27, 25, RGB565), FrameBuffer(asteroidTypeSprite[meteor_type[1]][0], 27, 25, RGB565), FrameBuffer(asteroidTypeSprite[meteor_type[2]][0], 27, 25, RGB565)]
sprite_asteroid_transparent = [asteroidTypeSprite[meteor_type[0]][1], asteroidTypeSprite[meteor_type[1]][1], asteroidTypeSprite[meteor_type[2]][1]]
sprite_cup = FrameBuffer(cupSprite[3], cupSprite[0], cupSprite[1], RGB565)
sprite_ship = FrameBuffer(shipSkinSprite[0][3], shipSkinSprite[0][0], shipSkinSprite[0][1], RGB565)
sprite_ship_transparent = shipSkinSprite[0][2]
sprite_laser = FrameBuffer(laserSkinSprite[0][3], laserSkinSprite[0][0], laserSkinSprite[0][1], RGB565)
sprite_laser_transparent = laserSkinSprite[0][2]
sprite_life2times = FrameBuffer(life2timesSprite[3], life2timesSprite[0], life2timesSprite[1], RGB565)
sprite_life = FrameBuffer(lifeSprite[3], lifeSprite[0], lifeSprite[1], RGB565)
sprite_alien = FrameBuffer(alienSprite[3], alienSprite[0], alienSprite[1], RGB565)
sprite_qr = FrameBuffer(qrSprite[2], qrSprite[0], qrSprite[1], MONO_HLSB)

sprite_hr = FrameBuffer(hrSprite[3], hrSprite[0], hrSprite[1], RGB565)
sprite_en = FrameBuffer(enSprite[3], enSprite[0], enSprite[1], RGB565)
sprite_de = FrameBuffer(deSprite[3], deSprite[0], deSprite[1], RGB565)

offsetX = 0

class LVK:
    selectX = 0
    selectY = 0
    inputt = ''
    shifted = False
    keyboardLowercaseText = [
      ["1","2","3","4","5","6","7","8","9","0","-","="],
      ["q","w","e","r","t","y","u","i","o","p","[","]","#"],
      ["a","s","d","f","g","h","j","k","l",";","\'"],
      ["\\","z","x","c","v","b","n","m",",",".","/"]
    ]
    keyboardUppercaseText = [
      ["!",'"',"£","$","%","^","&","*","(",")","_","+"],
      ["Q","W","E","R","T","Y","U","I","O","P","{","}","~"],
      ["A","S","D","F","G","H","J","K","L",":","@"],
      ["|","Z","X","C","V","B","N","M","<",">","?"]
    ]

    #Colors
    textSelectedClr = 0 #33808 #31
    textBgClr = 16904
    textClr = 65535

    @classmethod
    def drawKeyboard(cls):
        display.fill(16)
        for i in range(0,4):
            for j in range(0,13):
                try:
                    _ = cls.keyboardLowercaseText[i][j]
                    if cls.selectX == j and cls.selectY == i:
                        display.rect(j*8+offsetX, i*8, 8, 8, cls.textSelectedClr, True)
                    else:
                        display.rect(j*8+offsetX, i*8, 8, 8, cls.textBgClr, True)
                    if cls.shifted:
                        display.text(cls.keyboardUppercaseText[i][j], j*8+offsetX, i*8, cls.textClr)
                    else:
                        display.text(cls.keyboardLowercaseText[i][j], j*8+offsetX, i*8, cls.textClr)
                except IndexError:
                    pass
        if cls.selectX == 0 and cls.selectY == 4:
            display.rect(0+offsetX, 32, 24, 8, cls.textSelectedClr, True)
        else:
            display.rect(0+offsetX, 32, 24, 8, cls.textBgClr, True)
        display.text('ESC', 0+offsetX, 32, cls.textClr)
        if cls.selectX == 0 and cls.selectY == 5:
            display.rect(0+offsetX, 40, 40, 8, cls.textSelectedClr, True)
        else:
            display.rect(0+offsetX, 40, 40, 8, cls.textBgClr, True)
        display.text('ENTER', 0+offsetX, 40, cls.textClr)
        if cls.selectX == 1 and cls.selectY == 4:
            display.rect(24+offsetX, 32, 40, 8, cls.textSelectedClr, True)
        else:
            display.rect(24+offsetX, 32, 40, 8, cls.textBgClr, True)
        display.text('SPACE', 24+offsetX, 32, cls.textClr)
        if len(cls.inputt) > 16:
            display.text(cls.inputt[-16:], 0+offsetX, 120, cls.textClr)
        else:
            display.text(cls.inputt, 0+offsetX, 120, cls.textClr)
        display.text("A: Select", 0+offsetX, 48, cls.textClr)
        display.text("B: Backspace", 0+offsetX, 56, cls.textClr)
        display.text("C: Shift Toggle", 0+offsetX, 64, cls.textClr)
        display.commit()
    @classmethod
    def getMod(cls):
        if cls.selectY == 0:
            return 12
        elif cls.selectY == 1:
            return 13
        elif cls.selectY == 2 or cls.selectY == 3:
            return 11
        elif cls.selectY == 4:
            return 2
        else:
            return 1
    @classmethod
    def rightPress(cls):
        cls.selectX = (cls.selectX+1)%cls.getMod()
        cls.drawKeyboard()
    @classmethod
    def leftPress(cls):
        cls.selectX = (cls.selectX-1)%cls.getMod()
        cls.drawKeyboard()
    @classmethod
    def upPress(cls):
        cls.selectY = (cls.selectY-1)%6
        cls.selectX = max(0, min(cls.getMod()-1, cls.selectX))
        cls.drawKeyboard()
    @classmethod
    def downPress(cls):
        cls.selectY = (cls.selectY+1)%6
        cls.selectX = max(0, min(cls.getMod()-1, cls.selectX))
        cls.drawKeyboard()
    @classmethod
    def select(cls):
        try:
            if cls.shifted:
                cls.inputt = str(cls.inputt)+cls.keyboardUppercaseText[cls.selectY][cls.selectX]
            else:
                cls.inputt = str(cls.inputt)+cls.keyboardLowercaseText[cls.selectY][cls.selectX]
            cls.drawKeyboard()
            display.commit()
        except IndexError:
            if cls.selectX == 1 and cls.selectY == 4:
                cls.inputt = str(cls.inputt)+" "
                cls.drawKeyboard()
                display.commit()
            else:
                cls.end()
    @classmethod
    def init(cls):
        global menu
        cls.inputt = ""
        cls.selectX, cls.selectY = 0,0
        menu = 8
        cls.drawKeyboard()
    @classmethod
    def end(cls):
        global ssid, pswd, menu, select
        if cls.selectY == 5:
            if select == 0:
                ssid = cls.inputt
            elif select == 1:
                pswd = cls.inputt
        menu = 7
        networkMenu()
        scroll()
        display.commit()
        networkMenu()
        scroll()
        display.commit()
    @classmethod
    def shiftLock(cls):
        cls.shifted = not cls.shifted
        cls.drawKeyboard()
    @classmethod
    def backspace(cls):
        cls.inputt = cls.inputt[:-1]
        cls.drawKeyboard()

if wlan.isconnected():
  print('Connection OK')

import lang_strings as ls

lang_en = ls.en
lang_hr = ls.hr
lang_de = ls.de
lang_es = ls.es
lang_fr = ls.fr

select = 0
x = None
menu = 1
money = 0
laser = 0
meteors = 0
coinsUpg = 0
value = 0
shipPos = 1
shipX = -4
shipXchngBy = 52 #tu mijenjaj brzinu
meteorAY = -40
mAH = 3 #meteorAHealth
meteorBY = -40
mBH = 3
meteorCY = -40
mCH = 3
meteorKill = 63
meteorNoKill = 115
meteorsShotInSession = 0
fVA = 1 #fall value a,b,c
fVB = 2
fVC = 3
multi = 1
flicker = False
cupsList = [0,0,0,0,1,1,1,2] #  0 su vanzemaljci, 1 su +1 život, a 2 su +2 života
tone = True
code = 5
lives = 1
livesTick = 1
totalDistance = 0
lang = None
fastl = 0
selectMeteor = [0, 1, 0]
ssid = None
pswd = None
running = True
networks = None
unlockedSkins = [2, 0, 0, 1, 1] #0, 0, #

def save():
  with open('data.txt', 'w') as f:
    global money, laser, meteors, coinsUpg, tone, totalDistance, lang, fastl, skin, unlockedSkins
    f.write(str(money)+'\n')
    f.write(str(laser)+'\n')
    f.write(str(meteors)+'\n')
    f.write(str(coinsUpg)+'\n')
    f.write(str(tone)+'\n')
    f.write(str(totalDistance)+'\n')
    if lang == lang_en:
      f.write('en\n')
    elif lang == lang_hr:
      f.write('hr\n')
    elif lang == lang_de:
      f.write('de\n')
    elif lang == lang_es:
      f.write('es\n')
    elif lang == lang_fr:
      f.write('fr\n')
    f.write(str(fastl)+'\n')
    f.write(str(skin)+'\n')
    f.write(str(unlockedSkins)+'\n')

def load():
  try:
    with open('data.txt', 'r') as f:
      global money, laser, meteors, coinsUpg, tone, totalDistance, lang, fastl, skin, unlockedSkins
      money = float(f.readline().strip())
      laser = int(f.readline().strip())
      meteors = int(f.readline().strip())
      coinsUpg = int(f.readline().strip())
      tone = f.readline().strip() == 'True'
      totalDistance = int(f.readline().strip())
      lang = f.readline().strip()
      if lang == "en":
        lang = lang_en[:]
      elif lang == "hr":
        lang = lang_hr[:]
      elif lang == "de":
        lang = lang_de[:]
      elif lang == "es":
        lang = lang_es[:]
      elif lang == "fr":
        lang = lang_fr[:]
      fastl = int(f.readline().strip())
      skin = int(f.readline().strip())
      clean_elements = f.readline().strip().strip("[]").split(",")
      unlockedSkins = [int(i) for i in clean_elements]
  except:
    pass
  try:
    with open('wifi.txt', 'r') as f:
      global ssid, pswd
      ssid = f.readline().strip()
      pswd = f.readline().strip()
  except:
    pass

def langSelectOnStartup():
  global select, menu, laser, meteors, coinsUpg, value
  display.fill(0)
  display.text('SETUP '+lang[33], 64-len('SETUP '+lang[33])*4+offsetX, 0, 65535)
  display.text("English", 128-len("English")*8+offsetX, (0-select+4)*15, 65535)
  display.text("Hrvatski", 128-len("Hrvatski")*8+offsetX, (0-select+5)*15, 65535)
  display.text("Deutsch "+lang[34], 128-len("Deutsch "+lang[34])*8+offsetX, (0-select+6)*15, 65535)
  display.blit(sprite_en, 8+offsetX, (0-select+4)*15, 0)
  display.blit(sprite_hr, 8+offsetX, (0-select+5)*15, 0)
  display.blit(sprite_de, 8+offsetX, (0-select+6)*15, 65535)

def startup():
    display.fill(1234)
    display.blit(sprite_hr, 113, 0, 0)
    display.blit(sprite_en, 113, 8, 0)
    display.blit(sprite_de, 113, 16, 65535)
    for i in range(113,128,2):
        display.pixel(i, 24, 0)
    display.commit()
    time.sleep(1)
    global lang, menu
    load()
    if lang is None:
        lang = lang_en[:]
        menu = 12
        langSelectOnStartup()
        display.text('>', 0+offsetX, 60, 65535)
        display.commit()
    else:
        save()
        menu = 1
        display.fill(0)
        t1 = 'The Bit'
        t2 = 'Superstars'
        t3 = 'present...'
        display.text(t1, 64-len(t1)*4+offsetX, 52, 65535)
        display.text(t2, 64-len(t2)*4+offsetX, 60, 65535)
        display.text(t3, 64-len(t3)*4+offsetX, 68, 65535)
        display.commit()
        time.sleep(1.25)
        mainmenu()
        display.text(str(">"), 0+offsetX, 60, 65535)
        display.commit()

def setskin():
    global skin, sprite_ship, sprite_ship_transparent, sprite_laser, sprite_laser_transparent, sprite_asteroid, sprite_asteroid_transparent
    #default
    if skin == '683d5113-3ee2-41bd-96eb-8532b19acc6b':
        skinToSet = 0
    #french
    elif skin == '4df7f35e-1f99-46b0-ab23-098a273e3f92':
        skinToSet = 1
    #croatia
    elif skin == 'a59c3e34-5264-48b5-9daf-15dd051a14fa':
        skinToSet = 2
    #bus
    #elif skin == '232f7bc2-5264-4aef-977a-d3f3c7a0658e':
    #    skinToSet = 3
    #b2
    #elif skin == 'd4f134ac-0ce7-43cf-b5fc-4d4b4ac3560c':
    #    skinToSet = 4
    #school1
    elif skin == '5c5bbe41-fffe-44cd-a44e-ae47f8f05bfe':
        skinToSet = 3
    #school2
    elif skin == 'ecb90661-85f0-4263-8726-aa6795a2653e':
        skinToSet = 4
    #fallback
    else:
        skinToSet = 0

    if skinToSet == 3:
        meteor_type = [2,2,2]
    elif skinToSet == 4:
        meteor_type = [3,3,3]
    else:
        meteor_type = [0,0,0]

    sprite_ship = FrameBuffer(shipSkinSprite[skinToSet][3], shipSkinSprite[skinToSet][0], shipSkinSprite[skinToSet][1], RGB565)
    sprite_ship_transparent = shipSkinSprite[skinToSet][2]
    sprite_laser = FrameBuffer(laserSkinSprite[skinToSet][3], laserSkinSprite[skinToSet][0], laserSkinSprite[skinToSet][1], RGB565)
    sprite_laser_transparent = laserSkinSprite[skinToSet][2]
    sprite_asteroid = [FrameBuffer(asteroidTypeSprite[meteor_type[0]][0], 27, 25, RGB565),
                       FrameBuffer(asteroidTypeSprite[meteor_type[1]][0], 27, 25, RGB565),
                       FrameBuffer(asteroidTypeSprite[meteor_type[2]][0], 27, 25, RGB565)]
    sprite_asteroid_transparent = [asteroidTypeSprite[meteor_type[0]][1],
                                   asteroidTypeSprite[meteor_type[1]][1],
                                   asteroidTypeSprite[meteor_type[2]][1]]

def shuffle(array):
    global lives, select, livesTick
    if array == cupsList:
        select = 0
        if lives > 1:
            livesTick = 125
        lives -= 1
    for i in range(len(array) - 1, 0, -1):
        j = randrange(i + 1)
        array[i], array[j] = array[j], array[i]

def shuffleMeteors():
    global selectMeteor, meteorAY, meteorBY, meteorCY
    while True:
        shuffle(selectMeteor)
        if (((meteorAY <= -25 or meteorAY >= 128) or selectMeteor[0]) and
            ((meteorBY <= -25 or meteorBY >= 128) or selectMeteor[1]) and
            ((meteorCY <= -25 or meteorCY >= 128) or selectMeteor[2])):
            break

def draw_new_menu_items(string, idx_in_menu):
    display.text(string, 64-len(string)*4+offsetX, (0-select+(idx_in_menu+4))*15, 65535)

def about():
  global menu, select
  menu = 4
  select = 0
  display.fill(16)
  display.text("Meteor Shooter", 8+offsetX, 0, 65535)
  display.text(lang[0], 64-len(lang[0])*4+offsetX, 8, 65535)
  display.text(version, 0+offsetX, 16, 65535)
  display.text(lang[1], 0+offsetX, 24, 65535)
  display.text("Adrian", 8+offsetX, 32, 65535)
  display.text("Leon", 8+offsetX, 40, 65535)
  display.text(lang[2], 0+offsetX, 56, 65535)
  display.text("Leon", 8+offsetX, 64, 65535)
  display.text(lang[32], 0+offsetX, 80, 65535)
  display.text("Leon", 8+offsetX, 88, 65535)
  display.text(lang[4], 64-len(lang[4])*4+offsetX, 120, 65535)
  display.commit()

def mainmenu():
  global select, x, menu, laser, meteors, coinsUpg, value
  display.fill(16)
  draw_new_menu_items(lang[5],0)
  draw_new_menu_items(lang[6],1)
  draw_new_menu_items(lang[7],2)
  draw_new_menu_items(lang[8],3)
  draw_new_menu_items(lang[38],4)
  draw_new_menu_items('QR', 5)
  draw_new_menu_items(lang[43], 6)
  display.rect(0+offsetX, 0, 128, 8, 16, 1)
  display.text("METEOR SHOOT>R", 8+offsetX, 0, 65535)

def mainmenu2():
  global select, x, menu, laser, meteors, coinsUpg, value, tone
  display.fill(16)
  temp = lang[9]+str(tone)
  draw_new_menu_items(temp,0)
  draw_new_menu_items(lang[33],1)
  draw_new_menu_items(lang[39],2)
  draw_new_menu_items(lang[40],3)
  draw_new_menu_items(lang[41],4)
  draw_new_menu_items(lang[26],5)
  draw_new_menu_items('Overclock',6)
  display.rect(0+offsetX, 0, 128, 8, 16, 1)
  display.text(lang[7], 64-len(lang[7])*4+offsetX, 0, 65535)

def onlineMenu():
    for i in range(5):
        draw_new_menu_items(f'item {i+1}', i)

def networkMenu():
    #lang[35] je ssid i lang[36] je lozinka
    global menu, select
    display.fill(16)
    draw_new_menu_items(lang[35], 0)
    draw_new_menu_items(lang[36], 1)
    draw_new_menu_items(lang[37], 2)
    display.rect(0+offsetX, 0, 128, 8, 16, 1)
    display.text(lang[26], 64-len(lang[26])*4+offsetX, 0, 65535)

def scanNetworks():
    global networks, wlan
    display.fill(16)
    display.text('...', 52+offsetX, 60, 65535)
    display.commit()
    networks = wlan.scan()

def listNetworks():
    global networks, wlan
    display.fill(16)
    display.text(lang[35], 64-len(lang[35])*4+offsetX, 0, 65535)
    draw_new_menu_items(lang[42], 0)
    for i in range(len(networks)):
        draw_new_menu_items(networks[i][0].decode(), i-5)

def skinitem():
  global select, x, menu, laser, meteors, coinsUpg, value, fastl
  display.blit(sprite_coin, 0+offsetX, 0, 0)
  display.text(str(money), 13+offsetX, 0, 65535)
  if select == 0:
    item = lang[44]
  elif select == 1:
    item = lang[45]
    value = 1000
  elif select == 2:
    item = lang[46]
    value = 1000
# elif select == 3:
#   item = lang[47]
#   value = 1000
# elif select == 4:
#   item = lang[48]
#   value = 1000
  elif select == 3:
    item = lang[49]
    value = 0
  elif select == 4:
    item = lang[50]
    value = 0
  else:
    item = 'ERR01'
  if unlockedSkins[select]:
    value = 9998 + unlockedSkins[select]
  display.blit(FrameBuffer(shipSkinSprite[select][3], shipSkinSprite[select][0], shipSkinSprite[select][1], RGB565),48,48,shipSkinSprite[select][2])
  display.blit(FrameBuffer(laserSkinSprite[select][3], laserSkinSprite[select][0], laserSkinSprite[select][1], RGB565),60,40,laserSkinSprite[select][2])
  display.text(str(item), 64-len(item)*4+offsetX, 24, 65535)
  if value == 9999:
    temp = "EQUIP"
  elif value == 10000:
    temp = "EQUIPPED"
  else:
    temp = value
  display.text(str(temp), 64-len(str(temp))*4+offsetX, 96, 65535)
  display.commit()

def appropriateMenu():
  if menu == 1:
    mainmenu()
  elif menu == 5:
    mainmenu2()
  elif menu == 6:
    langSelect()
  elif menu == 7:
    networkMenu()
  elif menu == 9:
    onlineMenu()
  elif menu == 11:
    listNetworks()
  elif menu == 12:
    langSelectOnStartup()

def scroll():
  global menu
  if menu == 1 or (5 <= menu <= 7) or (11 <= menu <= 12):
    appropriateMenu()
    display.text(">",0+offsetX,60,65535)
    display.commit()

def minigameSetup():
  global livesTick, lives
  shuffle(cupsList)
  if (livesTick == 0 and lives <= 0) or (lives <= 0):
    minigame()

def drawgame():
  global shipX, meteorAY, meteorBY, meteorCY, money, coinsUpg, multi, lives, livesTick, shipPos
  display.fill(0)
  display.blit(sprite_ship, shipX+3+offsetX, 80, sprite_ship_transparent)
  display.blit(sprite_asteroid[0], 0+offsetX, int(meteorAY), sprite_asteroid_transparent[0])
  display.blit(sprite_asteroid[1], 52+offsetX, int(meteorBY), sprite_asteroid_transparent[1])
  display.blit(sprite_asteroid[2], 104+offsetX, int(meteorCY), sprite_asteroid_transparent[2])
  shipPos = ((shipX+4)/52)+1
  display.blit(sprite_coin, 0+offsetX, 0, 0)
  display.text(f'{money}', 13+offsetX, 0, 65535)
  display.text(f'{coinsUpg}', 0+offsetX, 12, 65535)
  if multi > 1:
    display.text(f'x{multi}', 8+offsetX, 12, 65535)
  display.blit(sprite_life, 0+offsetX, 20, 0)
  display.text(f'{lives},{livesTick}', 11+offsetX, 20, 65535)

def game():
  global totalDistance, livesTick, lives, shipX, meteorAY, meteorBY, meteorCY, shipPos, money, meteorKill, meteorNoKill, fVA, fVB, fVC, meteorsShotInSession, multi, menu
  totalDistance += 1
  drawgame()
  if meteorsShotInSession == 0:
    multi = 1
    fVC = 7/4
  elif meteorsShotInSession == 10:
    if fVC != 5/4:
      if tone: piezo.tone(500, 150)
      if tone: piezo.tone(1000, 150)
    fVC = 5/4
  elif meteorsShotInSession == 25:
    if fVA != 3:
      if tone: piezo.tone(500, 150)
      if tone: piezo.tone(1000, 150)
    fVA = 3
    fVB = 3
    fVC = 1
  elif meteorsShotInSession == 40:
    if fVC != 3/4:
      if tone: piezo.tone(500, 150)
      if tone: piezo.tone(1000, 150)
    fVC = 3/4
    multi = 5/4
  elif meteorsShotInSession == 65:
    if fVC != 3/5:
      if tone: piezo.tone(500, 150)
      if tone: piezo.tone(1000, 150)
    fVC = 3/5
    multi = 3/2
  elif meteorsShotInSession == 100:
    if fVC != 1:
      if tone: piezo.tone(1500, 150)
      if tone: piezo.tone(2000, 150)
    fVC = 1
    fVA = 5
    fVB = 7
    multi = 2
  display.commit()
  if livesTick == 0:
    if shipPos == 1 and meteorNoKill > meteorAY > meteorKill:
      minigameSetup()
    elif shipPos == 2 and meteorNoKill > meteorBY > meteorKill:
      minigameSetup()
    elif shipPos == 3 and meteorNoKill > meteorCY > meteorKill:
      minigameSetup()
  if livesTick > 0:
    livesTick -= 1

def posBoxX():
    if select == 0 or select == 3 or select == 5:
        return 0
    elif select == 1 or select == 6:
        return 43
    else:
        return 86

def posBoxY():
    global select
    if select <= 2:
        return 0
    elif select == 3 or select == 4:
        return 43
    else:
        return 86

def minigame(aPressed=False): #nedovršeno
  global menu, select, lives, livesTick, cupsList
  menu = 10
  if not aPressed:
    display.fill(0)
    _cupPos = (
        (00, 00), (43, 00), (86, 00),
        (00, 43),           (86, 43),
        (00, 86), (43, 86), (86, 86)
    )
    for cupx, cupy in _cupPos:
        display.blit(sprite_cup, cupx+offsetX, cupy, 0)
    item = "A:"
    item2 = lang[10]
    item3 = "B:"
    item4 = lang[11]
    item5 = lang[12]
    display.text(item, 64-len(item)*4+offsetX, 48, 65535)
    display.text(item2, 64-len(item2)*4+offsetX, 56, 65535)
    display.text(item3, 64-len(item3)*4+offsetX, 64, 65535)
    display.text(item4, 64-len(item4)*4+offsetX, 72, 65535)
    display.text(item5, 64-len(item5)*4+offsetX, 80, 65535)
    display.rect(posBoxX()+offsetX, posBoxY(), 40, 40, 65535, 0)
    display.commit()
  else:
    for i in range(44,14,-1):
      display.fill(0)
      display.blit(sprite_cup, 44+offsetX, i, 0)
      display.commit()
    item = cupsList[select]
    if item == 0:
      display.blit(sprite_alien, 53+offsetX, 50, 0)
    elif item == 1:
      display.blit(sprite_life, 59+offsetX, 50, 0)
    elif item == 2:
      display.blit(sprite_life2times, 49+offsetX, 50, 0)
    display.commit()
    time.sleep(1)
    lives += item
    if lives <= 0:
      menuButton()
    else:
      livesTick = 125
      menu = 0

def buymenu():
  global select, x, menu, laser, meteors, coinsUpg, value
  display.fill(16)
  display.blit(sprite_coin, 0+offsetX, 0, 0)
  display.text(str(money), 13+offsetX, 0, 65535)
  display.rect(32+offsetX, 32, 64, 64, 0, 1)
  display.rect(0+offsetX, 40, 16, 48, 0, 1)
  display.rect(112+offsetX, 40, 16, 48, 0, 1)
  if menu == 2: shopitem()
  elif menu == 13: skinitem()

def buyscrollr(startValue, targetValue, step):
  global select, x, menu, laser, meteors, coinsUpg, value
  i = startValue
  while i != targetValue:
    i = i - step 
    display.fill(16)
    display.blit(sprite_coin, 0+offsetX, 0, 0)
    display.text(str(money), 13+offsetX, 0, 65535)
    display.rect(40 + i+offsetX, 40, 48, 48, 0, 1)
    display.rect(-32 + i+offsetX, 40, 48, 48, 0, 1)
    display.rect(112 + i+offsetX, 40, 48, 48, 0, 1)
    display.rect(-72 + i+offsetX, 40, 16, 48, 0, 1)
    display.rect(184 + i+offsetX, 40, 48, 48, 0, 1)
    display.commit()

def buymenu2(startValue, targetValue, step):
  global select, x, menu, laser, meteors, coinsUpg, value
  i = startValue
  while i != targetValue:
    i = i - step
    display.fill(16)
    display.blit(sprite_coin, 0+offsetX, 0, 0)
    display.text(str(money), 13+offsetX, 0, 65535)
    display.rect(int(40-i/2+offsetX), int(40-i/2),48+i,48+i,0,1)
    display.rect(0+offsetX, 40, 16, 48, 0, 1)
    display.rect(112+offsetX, 40, 16, 48, 0, 1)
    display.commit()

def shopitem():
  global select, x, menu, laser, meteors, coinsUpg, value, fastl
  display.blit(sprite_coin, 0+offsetX, 0, 0)
  display.text(str(money), 13+offsetX, 0, 65535)
  item2 = 'ERROR'
  if select == 0:
    item = lang[13]
    item2 = lang[14]
    if laser == 0:
      value = 100
    elif laser == 1:
      value = 150
    elif laser == 2:
      value = 9999
  elif select == 1:
    item = lang[15]
    item2 = lang[16]
    if meteors == 0:
      value = 50
    elif meteors == 1:
      value = 75
    elif meteors == 2:
      value = 9999
  elif select == 2:
    item = lang[15]
    item2 = lang[17]
    if coinsUpg == 0:
      value = 25
    elif coinsUpg == 1:
      value = 50
    elif coinsUpg == 2:
      value = 75
    elif coinsUpg == 3:
      value = 100
    elif coinsUpg == 4:
      value = 150
    elif coinsUpg == 5:
      value = 9999
  elif select == 3:
      item = lang[31]
      item2 = lang[14]
      if fastl == 0:
        value = 250
      elif fastl == 1:
        value = 300
      elif fastl == 2:
        value = 9999
  else:
    item = 'ERR01'
  display.text(str(item), 64-len(item)*4+offsetX, 56, 65535)
  display.text(str(item2), 64-len(item2)*4+offsetX, 64, 65535)
  if value == 9999:
    temp = "MAX"
  else:
    temp = value
  display.text(str(temp), 64-len(str(temp))*4+offsetX, 96, 65535)
  display.commit()

def helps():
  global menu, money, multi, coinsUpg
  menu = 3
  display.fill(0)
  display.blit(sprite_coin, 0+offsetX, 0, 0)
  display.text('123', 13+offsetX, 0, 65535)
  display.text('2x1.5', 0+offsetX, 12, 65535)
  display.blit(sprite_life, 0+offsetX, 20, 0)
  display.text('1,0', 11+offsetX, 20, 65535)
  item = 'ERROR'
  item2 = lang[22]
  item3 = lang[23]
  if select == 0:
    display.text(lang[18], 40+offsetX, 0, 65535)
    item = lang[21]+"1/4"
  elif select == 1:
    display.text(lang[24], 40+offsetX, 12, 65535)
    display.text(lang[25], 40+offsetX, 20, 65535)
    display.text(lang[19], 40+offsetX, 28, 65535)
    display.text(lang[20], 40+offsetX, 36, 65535)
    item = lang[21]+"2/4"
  elif select == 2:
  # display.text(lang[24], 40+offsetX, 12, 65535)
  # display.text(lang[25], 40+offsetX, 18, 65535)
  # display.text(lang[19], 40+offsetX, 8, 65535)
  # display.text(lang[20], 40+offsetX, 16, 65535)
    item = lang[21]+"3/4"
  elif select == 3:
    display.text(lang[27], 0+offsetX, 40, 65535)
    display.text(lang[28], 0+offsetX, 48, 65535)
    display.text(lang[29], 0+offsetX, 56, 65535)
    item = lang[21]+"4/4"
    item2 = lang[30]
  display.text(str(item), 64 - len(item) * 4+offsetX, 104, 65535)
  display.text(str(item2), 64 - len(item2) * 4+offsetX, 112, 65535)
  display.text(str(item3), 64 - len(item3) * 4+offsetX, 120, 65535)
  display.commit()

def gamePrep():
  global select, menu, shipX, meteorAY, meteorBY, meteorCY, meteorsShotInSession, fVA, fVB, fVC, lives, meteors, selectMeteor, mAH, mBH, mCH
  select = 0
  menu = 0
  shipX = -4
  meteorAY = -40
  mAH = 3
  meteorBY = -40
  mBH = 3
  meteorCY = -40
  mCH = 3
  meteorsShotInSession = 0
  fVA = 2
  fVB = 3
  fVC = 7/4
  lives = 1
  if meteors == 0:
      selectMeteor = [0, 1, 0]
  elif meteors == 1:
      selectMeteor = [1, 0, 1]
  elif meteors == 2:
      selectMeteor = [1, 1, 1]
  shuffleMeteors()
  game()

def selectModulo():
  global networks
  if menu == 1:
    return 7
  elif menu == 5:
    return 7
  elif menu == 6 or menu == 12:
    return 3
  elif menu == 7:
    return 3
  elif menu == 11:
    temp = len(networks)+1
    return temp

def drawlaser(untilWhere):
  global shipX, fastl
  i = 79
  while not i <= untilWhere+20:
    drawgame()
    display.blit(sprite_laser, shipX+15+offsetX, i, sprite_laser_transparent)
    display.commit()
    i -= fastl+3

def shootlaser():
  global fastl, meteorAY, meteorBY, meteorCY, money, coinsUpg, multi, meteorsShotInSession, shipPos, tone, mAH, mBH, mCH
  if tone: piezo.tone(1000,50)
  if shipPos == 1:
    drawlaser(meteorAY)
    if meteorKill > meteorAY >= -20:
      mAH -= laser+1
      if mAH <= 0:
        mAH = 3
        meteorAY = -40
        money += (coinsUpg + 1)*multi
        meteorsShotInSession += 1
        shuffleMeteors()
  elif shipPos == 2:
    drawlaser(meteorBY)
    if meteorKill > meteorBY >= -20:
      mBH -= laser+1
      if mBH <= 0:
        mBH = 3
        meteorBY = -40
        money += (coinsUpg + 1)*multi
        meteorsShotInSession += 1
        shuffleMeteors()
  elif shipPos == 3:
    drawlaser(meteorCY)
    if meteorKill > meteorCY >= -20:
      mCH -= laser+1
      if mCH <= 0:
        mCH = 3
        meteorCY = -40
        money += (coinsUpg + 1)*multi
        meteorsShotInSession += 1
        shuffleMeteors()

def langSelect():
  global select, x, menu, laser, meteors, coinsUpg, value
  display.fill(16)
  display.text(lang[33], 64-len(lang[33])*4+offsetX, 0, 65535)
  display.text("English", 128-len("English")*8+offsetX, (0-select+4)*15, 65535)
  display.text("Hrvatski", 128-len("Hrvatski")*8+offsetX, (0-select+5)*15, 65535)
  display.text("Deutsch "+lang[34], 128-len("Deutsch "+lang[34])*8+offsetX, (0-select+6)*15, 65535)
  display.blit(sprite_en, 8+offsetX, (0-select+4)*15, 0)
  display.blit(sprite_hr, 8+offsetX, (0-select+5)*15, 0)
  display.blit(sprite_de, 8+offsetX, (0-select+6)*15, 65535)

def wifi_connect_request():
  display.fill(16)
  display.text('...', 52+offsetX, 60, 65535)
  display.commit()
  if any(net[0].decode() == ssid for net in wlan.scan()):
    global ssid, pswd
    with open('wifi.txt', 'w') as f:
      f.write(ssid + '\n')
      f.write(pswd + '\n')
    save()
    wlan.disconnect()
    machine.soft_reset()

def downButton():
  global select, x, menu, laser, meteors, coinsUpg, value
  if selectModulo():
    select = (select+1)%selectModulo()
    scroll()
  elif menu == 8:
    LVK.downPress()
buttons.on_press(down_button, downButton)

def upButton():
  global select, x, menu, laser, meteors, coinsUpg, value
  if selectModulo():
    select = (select-1)%selectModulo()
    scroll()
  elif menu == 8:
    LVK.upPress()
buttons.on_press(up_button, upButton)

def aButton():
  global ssid, pswd, fastl, tone, code, select, x, menu, money, laser, meteors, coinsUpg, value, shipX, shipPos, meteorAY, meteorBY, meteorCY, meteorsShotInSession, fVA, fVB, fVC, multi, lang, unlockedSkins, skin
  if menu == 0:
    shootlaser()
  elif menu == 1:
    if select == 0:
      select = 0
      helps()
    elif select == 1:
      select = 0
      menu = 2
      buymenu()
    elif select == 2:
      menu = 5
      select = 0
      mainmenu2()
      display.text(">",0+offsetX,60,65535)
      display.commit()
    elif select == 3:
      menu = 4
      about()
    elif select == 4:
      pass
    elif select == 5:
      global running
      running = False
      save()
      display.fill(65535)
      display.blit(sprite_qr, 0, 0, 0)
      display.commit()
    elif select == 6:
      #default
      if skin == '683d5113-3ee2-41bd-96eb-8532b19acc6b':
        select = 0
      #french
      elif skin == '4df7f35e-1f99-46b0-ab23-098a273e3f92':
        select = 1
      #croatia
      elif skin == 'a59c3e34-5264-48b5-9daf-15dd051a14fa':
        select = 2
      #bus
     #elif skin == '232f7bc2-5264-4aef-977a-d3f3c7a0658e':
     #  select = 3
      #b2
     #elif skin == 'd4f134ac-0ce7-43cf-b5fc-4d4b4ac3560c':
     #  select = 4
      #school1
      elif skin == '5c5bbe41-fffe-44cd-a44e-ae47f8f05bfe':
        select = 3
      #school2
      elif skin == 'ecb90661-85f0-4263-8726-aa6795a2653e':
        select = 4
      #fallback
      else:
        select = 0
      menu = 13
      buymenu()
  elif menu == 2:
    if value != 9999 and money >= value:
      if tone: piezo.tone(200, 50)
      money -= value
      if select == 0:
        laser += 1
      elif select == 1:
        meteors += 1
      elif select == 2:
        coinsUpg += 1
      elif select == 3:
        fastl += 1
      save()
      buymenu()
      shopitem()
    else:
      temp = value != 9999
      if temp:
        display.text(str(money), 13+offsetX, 0, 63488)
        display.commit()
      if tone: piezo.tone(125, 50)
      time.sleep(0.25)
      if temp:
        display.text(str(money), 13+offsetX, 0, 65535)
        display.commit()
  elif menu == 3:
    if select == 3:
      menu = 0
      gamePrep()
    else:
      select += 1
      helps()
  elif menu == 5:
    if select == 0:
      tone = not tone
      mainmenu2()
      display.text(">",0+offsetX,60,65535)
      display.commit()
    elif select == 1:
      menu = 6
      if lang == lang_en:
        select = 0
      elif lang == lang_hr:
        select = 1
      elif lang == lang_de:
        select = 2
      langSelect()
      display.text(">",0+offsetX,60,65535)
      display.commit()
    elif select == 2:
      save()
      print('Save OK')
      display.text(lang[39],64-len(lang[39])*4+offsetX,60,16)
      display.text('OK',56+offsetX,60,65535)
      display.commit()
    elif select == 3:
      global money, laser, meteors, coinsUpg, tone, totalDistance, lang, fastl, ssid, pswd
      money = 0
      laser = 0
      meteors = 0
      coinsUpg = 0
      tone = True
      totalDistance = 0
      fastl = 0
      ssid = None
      pswd = None
      import os
      try: os.remove('data.txt')
      except OSError: pass
      try: os.remove('wifi.txt')
      except OSError: pass
      print('Reset OK')
      display.text(lang[40],64-len(lang[40])*4+offsetX,60,16)
      display.text('OK',56+offsetX,60,65535)
      display.commit()
    elif select == 4:
      save()
      machine.soft_reset()
    elif select == 5:
      menu = 7
      select = 0
      networkMenu()
      display.text(">",0+offsetX,60,65535)
      display.commit()
    elif select == 6:
      _freq = None
      while _freq not in [80,160,240]:
        try:
          _freq = int(input('which MHz: '))
        except Exception as e:
          print(str(e))
        if _freq not in [80,160,240]:
          print('plz 80, 160 or 240 MHz ok?\nno less due to wifi')
      machine.freq(_freq*1000000)
      print('ok')
  elif menu == 6:
    if select == 0:
      lang = lang_en[:]
    elif select == 1:
      lang = lang_hr[:]
    elif select == 2:
      lang = lang_de[:]
    menu = 5
    select = 1
    mainmenu2()
    display.text(">",0+offsetX,60,65535)
    display.commit()
  elif menu == 7:
      if select == 0:
          menu = 11
          select = 0
          scanNetworks()
          listNetworks()
          display.text(">",0+offsetX,60,65535)
          display.commit()
      elif select == 1:
          LVK.init()
      elif select == 2:
          print(ssid,pswd)
          if not (ssid is None or pswd is None):
              wifi_connect_request()
  elif menu == 8:
      LVK.select()
  elif menu == 10:
      minigame(True)
  elif menu == 11:
      if select == 0:
          menu = 11
          select = 0
          scanNetworks()
          listNetworks()
          display.text(">",0+offsetX,60,65535)
          display.commit()
      else:
          ssid = networks[select-1][0].decode()
          menu = 7
          select = 0
          networkMenu()
          display.text(">",0+offsetX,60,65535)
          display.commit()
  elif menu == 12:
    if select == 0:
      lang = lang_en[:]
    elif select == 1:
      lang = lang_hr[:]
    elif select == 2:
      lang = lang_de[:]
    menu = 1
    select = 0
    display.fill(0)
    startup()
  elif menu == 13:
    temp = value < 9999
    if temp and money >= value:
      if tone: piezo.tone(200, 50)
      money -= value
      unlockedSkins[select] = 1
      buymenu()
      skinitem()
    else:
      if temp:
        display.text(str(money), 13+offsetX, 0, 63488)
        display.commit()
      if value == 9999:
        for i in range(len(unlockedSkins)):
          if unlockedSkins[i] == 2:
            unlockedSkins[i] = 1
        unlockedSkins[select] = 2
        #default
        if select == 0:
          skin = '683d5113-3ee2-41bd-96eb-8532b19acc6b'
        #french
        elif select == 1:
          skin = '4df7f35e-1f99-46b0-ab23-098a273e3f92'
        #croatia
        elif select == 2:
          skin = 'a59c3e34-5264-48b5-9daf-15dd051a14fa'
        #bus
        #elif select == 3:
        # skin = '232f7bc2-5264-4aef-977a-d3f3c7a0658e'
        #b2
        #elif select == 4:
        # skin = 'd4f134ac-0ce7-43cf-b5fc-4d4b4ac3560c'
        #school1
        elif select == 3:
          skin = '5c5bbe41-fffe-44cd-a44e-ae47f8f05bfe'
        #school2
        elif select == 4:
          skin = 'ecb90661-85f0-4263-8726-aa6795a2653e'
        #fallback
        else:
          skin = '683d5113-3ee2-41bd-96eb-8532b19acc6b'
        setskin()
        buymenu()
      if tone: piezo.tone(125, 50)
      time.sleep(0.25)
      if temp:
        display.text(str(money), 13+offsetX, 0, 65535)
        display.commit()
    save()
buttons.on_press(a_button, aButton)

def menuButton():
  global menu, select, money, code
  if menu == 0 or menu == 10:
    save()
    if tone: piezo.tone(1000, 150)
    if tone: piezo.tone(500, 150)
    select = 0
    menu = 1
    mainmenu()
    scroll()
  elif menu == 8:
    LVK.shiftLock()
buttons.on_press(menu_button, menuButton)

def bButton():
  global select, menu, laser, meteors, coinsUpg, value
  if menu == 2:
    menu = 1
    select = 1
    mainmenu()
    display.text(">",0+offsetX,60,65535)
    display.commit()
  elif menu == 4:
    menu = 1
    select = 3
    mainmenu()
    display.text(">",0+offsetX,60,65535)
    display.commit()
  elif menu == 5:
    menu = 1
    select = 2
    mainmenu()
    display.text(">",0+offsetX,60,65535)
    display.commit()
  elif 6 <= menu < 8:
    menu = 5
    select = 0
    mainmenu2()
    display.text(">",0+offsetX,60,65535)
    display.commit()
  elif menu == 3:
    menu = 0
    gamePrep()
  elif menu == 8:
    LVK.backspace()
  elif menu == 10:
    select += 1
    if tone: piezo.tone(200, 50)
    select = select % 8
  elif menu == 11:
    menu = 7
    select = 0
    networkMenu()
    display.text(">", 0+offsetX, 60, 65535)
    display.commit()
  elif menu == 13:
    menu = 1
    select = 6
    mainmenu()
    display.text(">",0+offsetX,60,65535)
    display.commit()
buttons.on_press(b_button, bButton)

def rightButton():
  global select, x, menu, laser, meteors, coinsUpg, value, shipX, shipXchngBy
  if menu == 0:
    shipX = shipX + shipXchngBy
    if shipX > 100:
      shipX = 100
    if tone: piezo.tone(200, 50)
    game()
  elif menu == 2:
    buymenu2(16, 0, 2)
    buyscrollr(0, -72, 3)
    buymenu2(0, 16, -2)
    select = (select+1)%4
    buymenu()
    shopitem()
  elif menu == 8:
    LVK.rightPress()
  elif menu == 13:
    buymenu2(16, 0, 2)
    buyscrollr(0, -72, 3)
    buymenu2(0, 16, -2)
    select = (select+1)%5
    buymenu()
    skinitem()
buttons.on_press(right_button, rightButton)

def leftButton():
  global select, x, menu, laser, meteors, coinsUpg, value, shipX, shipXchngBy
  if menu == 0:
    shipX = shipX - shipXchngBy
    if shipX < -4:
      shipX = -4
    if tone: piezo.tone(200, 50)
    game()
  elif menu == 2:
    buymenu2(16, 0, 2)
    buyscrollr(0, 72, -3)
    buymenu2(0, 16, -2)
    select = (select-1)%4
    buymenu()
    shopitem()
  elif menu == 8:
    LVK.leftPress()
  elif menu == 13:
    buymenu2(16, 0, 2)
    buyscrollr(0, 72, -3)
    buymenu2(0, 16, -2)
    select = (select-1)%5
    buymenu()
    skinitem()
buttons.on_press(left_button, leftButton)

allowed_versions = ['RELEASE', 'BETA', 'ALPHA']

if version_type in allowed_versions:
  print('Meteor Shooter',version)
  print('Za STEMIovu Školu budućnosti')
  print('GitHub: https://github.com/The-Bit-Superstars/Meteor-Shooter')
  startup()
  if menu == 1:
      mainmenu()
      display.text(str(">"),0+offsetX,60,65535)
      display.commit()
  while running:
    buttons.scan()
    if lives < 0:
      lives = 0
    if menu == 0:
      temp = random.randint(0,2)
      if temp == 0 and selectMeteor[0]:
        meteorAY += random.randint(fVA,fVB)/fVC
      elif temp == 1 and selectMeteor[1]:
        meteorBY += random.randint(fVA,fVB)/fVC
      elif temp == 2 and selectMeteor[2]:
        meteorCY += random.randint(fVA,fVB)/fVC
      if meteorAY >= 130:
        mAH = 3
        meteorAY = -40
        shuffleMeteors()
        minigameSetup()
      elif meteorBY >= 130:
        mBH = 3
        meteorBY = -40
        shuffleMeteors()
        minigameSetup()
      elif meteorCY >= 130:
        mCH = 3
        meteorCY = -40
        shuffleMeteors()
        minigameSetup()
      game()
    elif menu == 10:
        minigame()
    if flicker:
      if menu == 0 or menu == 3:
        display.fill(0)
        display.commit()
        if menu == 3:
          help()
else:
  print('fallback, while True loop escaped')
  strings = [
   ################****     < ovo su 16 hashtaga i 4 zvjezdice koji označuju koliko stane na ekran
  'why did you put ',        # koristi hashtagove za Bit/Codee, a sve za Chatter
  'this on your Bit',
  'or whichever    ',
  'device?         ',
  'this is a       ',
 f'{version_type}  ',
  'version so...   ',
  '                ',
  'GET OUT         '
  ]
  for i in range(0,len(strings)):
      if not strings[i] == version_type:
          display.text(strings[i], 0, i*8, 65535)
      else:
          display.text(strings[i], 0, i*8, 0x0ff0)
  display.text(version, 0, 112, 0xf00f)
  display.text(version_type, 0, 120, 0xf00f)
  display.commit()
