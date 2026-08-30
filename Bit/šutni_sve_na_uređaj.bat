@echo off
echo Kopiranje...

mpy-cross files.py
mpy-cross sprite_data.py
mpremote resume cp files.mpy :files.mpy
mpremote resume cp sprite_data.mpy :sprite_data.mpy
rm files.mpy sprite_data.mpy
mpremote resume cp lang_strings.py :lang_strings.py
mpremote resume cp main.py :main.py
mpremote resume cp boot.py :boot.py

mpremote resume cp alien.rgb565 :alien.rgb565
mpremote resume cp coin.rgb565 :coin.rgb565
mpremote resume cp cup.rgb565 :cup.rgb565
mpremote resume cp life.rgb565 :life.rgb565
mpremote resume cp life2times.rgb565 :life2times.rgb565
mpremote resume cp qr.mhlsb :qr.mhlsb

mpremote resume mkdir flags
mpremote resume cp flags/de.rgb565 :flags/de.rgb565
mpremote resume cp flags/en.rgb565 :flags/en.rgb565
mpremote resume cp flags/hr.rgb565 :flags/hr.rgb565

mpremote resume mkdir skins

mpremote resume mkdir skins/ships
mpremote resume cp skins/ships/default.rgb565 :skins/ships/default.rgb565
mpremote resume cp skins/ships/french.rgb565 :skins/ships/french.rgb565
mpremote resume cp skins/ships/croatia.rgb565 :skins/ships/croatia.rgb565
mpremote resume cp skins/ships/school1.rgb565 :skins/ships/school1.rgb565
mpremote resume cp skins/ships/school2.rgb565 :skins/ships/school2.rgb565

mpremote resume mkdir skins/lasers
mpremote resume cp skins/lasers/default.rgb565 :skins/lasers/default.rgb565
mpremote resume cp skins/lasers/french.rgb565 :skins/lasers/french.rgb565
mpremote resume cp skins/lasers/croatia.rgb565 :skins/lasers/croatia.rgb565
mpremote resume cp skins/lasers/school.rgb565 :skins/lasers/school.rgb565

echo Kopirano! Samo napravi reset.