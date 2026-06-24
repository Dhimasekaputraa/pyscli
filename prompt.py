import os
import getpass
import socket

def get_user_info():
    try :
        username = getpass.getuser()
    except Exception :
        username = os.environ.get("USER") or os.environ.get("USERNAME") or "USER"
    
    hostname = socket.gethostname()

    return {
        "user": username,
        "host": hostname
    }

def format_path(max_depth=3):
    cwd = os.getcwd()
    home = os.path.expanduser("~")

    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    parts = cwd.split(os.sep)

    if len(parts) > max_depth:
        cwd = os.sep.join(
            ["..."]+ parts[-2:]
        )

    return cwd


def get_prompt():
    user_info = get_user_info()
    cwd = format_path()

    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    return f"\n{GREEN}{user_info['user']}{RESET} | {BLUE}{user_info['host']}{RESET} : {cwd}$ "
