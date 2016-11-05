EXE_FILES=~/bin/pi_bot-user_interface
EXE=~/bin/pi_bot_ui

all:
	mkdir -p $(EXE_FILES)/
	cp -r *.py $(EXE_FILES)/
	echo "#!/bin/bash\npython3 $(EXE_FILES)" > $(EXE)
	chmod +x $(EXE)
install:
	sudo apt-get install expect
