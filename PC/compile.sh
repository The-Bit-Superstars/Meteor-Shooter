#!/usr/bin/env bash

python3 -m PyInstaller --clean --onefile --noconsole --optimize 2 --add-data="assets:assets" "Meteor Shooter.py"
