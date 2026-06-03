import sys
import os

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
        print(" exit    - Exit the shell")

    def change_directory(self):
        pass

    def current_directory(self):
        pass
        
    def exit_shell():
        sys.exit(0)

    def execute_commands(self):
        match self.command:
            case "help":
                Command.show_commands()
            case "cd":
                Command.change_directory(self)
            case "pwd":
                Command.current_directory(self)
            case "exit":
                Command.exit_shell()
