import subprocess
from time import time

def command(string):
    return string.split(' ')

sr = subprocess.run

version = subprocess.check_output(
    command('git describe --dirty --always'),
    text=True
).strip()
with open("main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
lines[51] = f"info = 'git: {version}, time: {int(time())}'\n"
with open("main.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

try:
    print('Kopiranje...')

    sr(command('mpy-cross files.py'), check=False)
    sr(command('mpy-cross sprite_data.py'), check=False)
    sr(command('mpy-cross main.py'), check=False)
    sr(command('mpremote resume cp files.mpy :files.mpy'), check=False)
    sr(command('mpremote resume cp sprite_data.mpy :sprite_data.mpy'), check=False)
    sr(command('mpremote resume cp main.mpy :game.mpy'), check=False)
    with open("launcher.py", "w", encoding="utf-8") as f:
        f.writelines('import game\n')
    sr(command('mpremote resume cp launcher.py :main.py'), check=False)
    sr(command('rm files.mpy sprite_data.mpy main.mpy launcher.py'), check=False)
    sr(command('mpremote resume cp lang_strings.py :lang_strings.py'), check=False)
    sr(command('mpremote resume cp boot.py :boot.py'), check=False)

    sr(command('mpremote resume cp alien.rgb565 :alien.rgb565'), check=False)
    sr(command('mpremote resume cp coin.rgb565 :coin.rgb565'), check=False)
    sr(command('mpremote resume cp cup.rgb565 :cup.rgb565'), check=False)
    sr(command('mpremote resume cp life.rgb565 :life.rgb565'), check=False)
    sr(command('mpremote resume cp life2times.rgb565 :life2times.rgb565'), check=False)
    sr(command('mpremote resume cp qr.mhlsb :qr.mhlsb'), check=False)

    sr(command('mpremote resume mkdir flags'), check=False)
    sr(command('mpremote resume cp flags/de.rgb565 :flags/de.rgb565'), check=False)
    sr(command('mpremote resume cp flags/en.rgb565 :flags/en.rgb565'), check=False)
    sr(command('mpremote resume cp flags/hr.rgb565 :flags/hr.rgb565'), check=False)

    sr(command('mpremote resume mkdir skins'), check=False)

    sr(command('mpremote resume mkdir skins/ships'), check=False)
    sr(command('mpremote resume cp skins/ships/default.rgb565 :skins/ships/default.rgb565'), check=False)
    sr(command('mpremote resume cp skins/ships/french.rgb565 :skins/ships/french.rgb565'), check=False)
    sr(command('mpremote resume cp skins/ships/croatia.rgb565 :skins/ships/croatia.rgb565'), check=False)
    sr(command('mpremote resume cp skins/ships/school1.rgb565 :skins/ships/school1.rgb565'), check=False)
    sr(command('mpremote resume cp skins/ships/school2.rgb565 :skins/ships/school2.rgb565'), check=False)

    sr(command('mpremote resume mkdir skins/lasers'), check=False)
    sr(command('mpremote resume cp skins/lasers/default.rgb565 :skins/lasers/default.rgb565'), check=False)
    sr(command('mpremote resume cp skins/lasers/french.rgb565 :skins/lasers/french.rgb565'), check=False)
    sr(command('mpremote resume cp skins/lasers/croatia.rgb565 :skins/lasers/croatia.rgb565'), check=False)
    sr(command('mpremote resume cp skins/lasers/school.rgb565 :skins/lasers/school.rgb565'), check=False)

    print('Kopirano! Samo napravi reset.')
except subprocess.CalledProcessError as e:
    print(repr(e))
