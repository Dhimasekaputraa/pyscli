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
        print(" exit    - Exit the shell")
        
    def exit_shell():
        sys.exit(0)

    def execute_commands(self):
        match self.command:
            case "help":
                Command.show_commands()
            case "exit":
                Command.exit_shell()
