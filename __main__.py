#!/usr/bin/python3
from user_interface import user_interface
if __name__ == "__main__":
	ui = user_interface()
	ui.update_user_interface()
	ui.window.root.mainloop()
