# dotty
Everquest Dot Tracker

Work in progress, please pardon the mess.

Only Necromancer is supported at the moment

# build

pip install pyinstaller

pyinstaller --onefile -w .\ui.py


# Executable


dist/dotty.exe
* Run EQ in any not fullscreen mode
* In game: /log on 
* Run dotty.exe
* Select log file to parse:  `{EQ_DIR}/Logs/eqlog_Gent_mischief.txt`
* Veiw window - timers won't be perfect, but they will be close

dist/replayLog.bat
* Run replayLog.bat
* Select log file to parse:  `{EQ_DIR}/Logs/eqlog_Gent_mischief.txt`
* Veiw window - This will replay your log file from the beginning.  It can be kinda fun to watch
