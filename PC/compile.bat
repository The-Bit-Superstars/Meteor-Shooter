echo off
py -3.12 -m PyInstaller --clean --onefile --noconsole --optimize 2 --add-data="assets:assets" "Meteor Shooter.py"
echo on
