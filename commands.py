import sys
import os
import getpass
import socket
import platform
import subprocess

class Command:
    def __init__(self, command, args):
        self.command = command
        self.args = args
        self.built_in_command = ["help", "exit", "cd", "pwd"]

    @staticmethod
    def show_commands():
        print("Available commands:")
        print(" help    - Show this help message")
        print(" mkdir   - Create a new directory")
        print(" cd      - Change directory")
        print(" ls      - List directory")
        print(" pwd     - Current working directory")
        print(" echo    - Print text to screen")
        print(" clear   - Removes visible screen")
        print(" exit    - Exit the shell")
    
    @staticmethod
    def get_user_info():
        try :
            username = getpass.getuser()
        except Exception :
            username = os.environ.get("USER") or os.environ.get("USERNAME") or "USER"
        
        hostname = socket.gethostname()
        os_name = platform.system()
        os_release = platform.release()

        return {
            "user": username,
            "host": hostname,
            "os": f"{os_name} {os_release}"
        }
    
    @staticmethod
    def format_path(max_depth=3):
        cwd = os.getcwd()
        home = os.path.expanduser("~")

        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]

        parts = cwd.split("/")

        if len(parts) > max_depth + 1:
            cwd = f".../{parts[-2]}/{parts[-1]}"

        return cwd
    
    @staticmethod
    def get_prompt():
        user_info = Command.get_user_info()
        cwd = Command.format_path()

        GREEN = "\033[32m"
        BLUE = "\033[34m"
        RESET = "\033[0m"

        return f"{GREEN}{user_info['user']}{RESET} | {BLUE}{user_info['host']}{RESET} : {cwd}$ "


    def external_commands(self):
        full_command = [self.command] + self.args
        try:
            subprocess.run(full_command, check=True)
        except FileNotFoundError:
            print(f"{self.command}: command not found")
        except subprocess.CalledProcessError:
            print(f"{self.command}: error executing command")
        except Exception as e:
            print(f"Error: {e}")

    def change_directory(self):
        target = self.args[0] if self.args else os.path.expanduser("~")
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except PermissionError:
            print(f"cd: {target}: Permission denied")

    def current_directory(self):
        print(os.getcwd())
        
    @staticmethod
    def exit_shell():
        sys.exit(0)

    def execute_commands(self):
        if self.command in self.built_in_command:
            match self.command:
                case "help":
                    Command.show_commands()
                case "cd":
                    self.change_directory()
                case "pwd":
                    self.current_directory()
                case "exit":
                    Command.exit_shell()
        else:
            self.external_commands()