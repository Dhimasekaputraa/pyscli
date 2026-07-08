import sys
import os
import config
from executor import Executor

class Command:

    def __init__(self, user_input, token, command, args):
        self.user_input = user_input
        self.token = token
        self.command = command
        self.args = args

    def show_commands(self):
        if len(self.args) > 1:
            print(f"{config.RED}help: too many arguments")
        if not self.args:
            print("Available commands:")
            print(" help        - Show this help message")
            print(" cd          - Change directory")
            print(" pwd         - Current working directory")
            print(" exit        - Exit the shell")
            print("To view external commands use : help --external")
        elif self.args == ["--external"]:
            print("External commands:")
            print(" ls | dir        - Displays a list of contents in the current active directory")
            print(" mkdir           - Create new directories")
            print(" rmdir           - Delete an empty directories")
            print(" cp | copy       - Copy files from one directory to another")
            print(" mv | move       - Move or rename files")
            print(" echo            - Print text to screen")
            print(" touch           - Create a file")
            print(" rm | del        - Remove file")
            print(" clear | cls     - Clear visible screen in shell")
            print(" cat | type      - Read a file")
            print(" grep | findstr  - Search specific text pattern")
            print(" sort            - Sort a string to ascending")
        else:
            print(f"{config.RED}help: only use help or help --external")

    def change_directory(self):
        target = self.args[0] if self.args else os.path.expanduser("~")
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"{config.RED}cd: {target}: No such file or directory")
        except PermissionError:
            print(f"{config.RED}cd: {target}: Permission denied")
    
    def current_directory(self):
        if self.args:
            print(f"{config.RED}pwd: too many arguments")
            return
        print(os.getcwd())

    def debug_mode(self):
        if self.args == ["--enable"]:
            if config.DEBUG == True:
                print(f"{config.YELLOW}debug: already in debug mode")
            else:
                config.DEBUG = True
                print(f"debug: entering debug mode...")
           
        elif self.args == ["--disable"]:
            if config.DEBUG == False:
                print(f"{config.YELLOW}debug: debug mode already disabled")
            else:
                config.DEBUG = False
                print(f"debug: leaving debug mode...")
        
        else:
            print(f"{config.RED}debug: use --enable or --disable flag")
    
    def check_ver(self):
        if self.args == ["--version"] or self.args == ["--v"]:
            print(f"{config.SHELLNAME} {config.GREEN}{config.VERSION}{config.RESET} " 
                  f"created by {config.BLUE}Ade Azhar, Adri Lorenzo, Dhimas Eka, Nugraha Bagya")
        else:
            print(f"{config.RED}pyscli: use --version or --v flag to check shell version")

    def exit_shell():
        print("さようなら...")
        sys.exit(0)

    def execute_commands(self):
        match self.command:
            case "help":
                Command.show_commands(self)
            case "cd":
                Command.change_directory(self)
            case "pwd":
                Command.current_directory(self)
            case "debug":
                Command.debug_mode(self)
            case "pyscli":
                Command.check_ver(self)
            case "exit":
                Command.exit_shell()
            case _:
                Executor.execute_external(
                    self.command, self.args
                )