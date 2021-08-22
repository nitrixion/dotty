# dotty
Everquest Dot Tracker

Work in progress, please pardon the mess.

Only Necromancer is supported at the moment

# build

pip install pyinstaller

pyinstaller --onefile -w .\ui.py


# Executable


dist/dotty.exe
* Run
* Select log file to parse:  `{EQ_DIR}/Logseqlog_Gent_mischief.txt`
* Run EQ in any not fullscreen mode
* Veiw window - timers won't be perfect, but they will be close

dist/replayLog.bat
* Run
* Select log file to parse:  `{EQ_DIR}/Logseqlog_Gent_mischief.txt`
* Veiw window - This will replay your log file from the beginning.  It can be kinda fun to watch