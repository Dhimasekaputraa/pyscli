import sys
import os
from executor import Executor

class Command:
    def __init__(self, user_input, token, command, args):
        self.user_input = user_input
        self.token = token
        self.command = command
        self.args = args

    def show_commands():
        print("Available commands:")
        print(" help    - Show this help message")
        print(" cd      - Change directory")
        print(" pwd     - Current working directory")
        print(" echo    - Print text to screen")
        print(" exit    - Exit the shell")

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
            print(os.getcwd(), "\n")
        elif self.args:
            print(*self.args, "\n")
            return

    def exit_shell():
        print("さようなら...")
        sys.exit(0)

    def execute_commands(self):
        match self.command:
            case "help":
                Command.show_commands()
            case "cd":
                Command.change_directory(self)
            case "pwd":
                Command.current_directory(self)
            case "echo":
                Command.print_text(self)
            case "exit":
                Command.exit_shell()
            case _:
                Executor.execute_external(
                    self.command, self.args
                )