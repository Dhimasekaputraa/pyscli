import sys
import os
from executor import Executor

class Command:
    debug = False

    def __init__(self, user_input, token, command, args):
        self.user_input = user_input
        self.token = token
        self.command = command
        self.args = args

    def show_commands(self):
        if len(self.args) > 1:
            print("help: too many arguments")
        if not self.args:
            print("Available commands:")
            print(" help        - Show this help message")
            print(" cd          - Change directory")
            print(" pwd         - Current working directory")
            print(" echo        - Print text to screen")
            print(" ls | dir    - Displays a list of contents in the current active directory")
            print(" mkdir       - Create new directories")
            print(" rmdir       - Delete an empty directories")
            print(" cp | copy   - Copy files from one directory to another")
            print(" mv | move   - Move or rename files")
            print(" exit        - Exit the shell")
        elif self.args == ["--external"]:
            print("External commands:")
            print(" touch           - Create a file")
            print(" rm | del        - Remove file")
            print(" clear | cls     - Clear visible screen in shell")
            print(" cat | type      - Read a file")
            print(" grep | findstr  - Search specific text pattern")
            print(" sort            - Sort a string to ascending")
        else:
            print("help: only write help or help --external")

    def change_directory(self):
        target = self.args[0] if self.args else os.path.expanduser("~")
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except PermissionError:
            print(f"cd: {target}: Permission denied")
    
    def current_directory(self):
        if self.args:
            print("pwd: too many arguments")
            return
        print(os.getcwd())

    def print_text(self):
        if self.args == ["$PWD"]:
            print(os.getcwd())
        elif self.args:
            print(*self.args)
            return
    
    def check_ver(self):
        if self.args == ["--version"] or self.args == ["--v"]:
            print(f"Pyscli 0.5.0 created by Ade Azhar, Adri Lorenzo, Dhimas Eka, Nugraha Bagya")
        else:
            print("pyscli: use --version or --v to check shell version")
    
    def debug_mode(self):
        if self.args == ["--enable"]:
            print(f"[SYSTEM] : entering debug mode...")
            Command.debug = True
           
        elif self.args == ["--disable"]:
            print(f"[SYSTEM] : leaving debug mode...")
            Command.debug = False
        
        else:
            print("debug: please use --enable or --disable")

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
            case "echo":
                Command.print_text(self)
            case "pyscli":
                Command.check_ver(self)
            case "exit":
                Command.exit_shell()
            case _:
                Executor.execute_external(
                    self.command, self.args
                )