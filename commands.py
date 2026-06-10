import sys
import os
import getpass
import socket
import platform

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
        print(" clear   - Removes visible screen")
        print(" exit    - Exit the shell")

    def change_directory(self):
        target = self.args[0] if self.args else os.path.expanduser("~")
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except PermissionError:
            print(f"cd: {target}: Permission denied")
    
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

    def current_directory(self):
        print(os.getcwd())

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

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
            case "clear":
                Command.clear_screen()
            case "exit":
                Command.exit_shell()
