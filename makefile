EXE_FILES=~/bin/pi_bot-user_interface
EXE=~/bin/pi_bot_ui
UPLOAD=~/bin/pi_bot_upload

all:
	mkdir -p $(EXE_FILES)/
	cp -r *.py $(EXE_FILES)/
	echo "#!/bin/bash\npython3 $(EXE_FILES)" > $(EXE)
	cat upload_script > $(UPLOAD)
	chmod +x $(EXE)
	chmod +x $(UPLOAD)
install:
	sudo apt-get install expect
