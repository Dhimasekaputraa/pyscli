import sys
import os
# import main

class Command:
    def __init__(self, user_input, token, command, args):
        self.user_input = user_input
        self.token = token
        self.command = command
        self.args = args

    def show_commands():
        print("Available commands:")
        print(" help  - Show this help message")
        print(" mkdir - Create a new directory")
        print(" cd    - Change directory")
        print(" ls    - list directory")
        print(" crf   - Create a new file")
        print(" pwd   - Current working directory")
        print(" exit  - Exit the shell")

    def create_directory(self):
        if not self.args:
            print("Usage: mkdir <directory_name>")
        else:
            try:
                os.mkdir(self.args[0])
            except FileExistsError:
                print(f"mkdir: cannot create directory '{self.args[0]}': File exists")
            except Exception as e:
                print(f"Error: {e}")

    def change_directory(self):
        try:
            os.chdir(self.args[0] if self.args else os.path.expanduser("~"))
        except FileNotFoundError:
            print(f"Bash: cd: {self.args[0]}: No such file or directory")
        except PermissionError:
            print(f"Bash: cd: {self.args[0]}: Permission denied")

    def list_directory(self):
        pass

    def current_directory(self):
        print(os.getcwd())
                
    def exit_shell():
        sys.exit(0)

    def execute_commands(self):
        match self.command:
            case "help":
                Command.show_commands()
            case "mkdir":
                Command.create_directory(self)
            case "cd":
                Command.change_directory(self)
            case "ls":
                pass
            case "pwd":
                Command.current_directory(self)
            case "crf":
                pass
            case "exit":
                Command.exit_shell()
