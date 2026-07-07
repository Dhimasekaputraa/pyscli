import os
import getpass
import socket
import shlex
import config
from commands import Command
from executor import Executor

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

def parse_and_execute(user_input):

    token = shlex.split(user_input)
    if not token:
        return
    
    if any(op in token for op in ("|", "<", ">", ">>")):
        commands = []
        current = []

        stdin = None
        stdout = None
        append = False

        i = 0

        while i < len(token):
            t = token[i]

            if t == "|":
                commands.append((current[0].lower(), current[1:]))
                current = []

            elif t == "<":
                stdin = token[i + 1]
                i += 1
            
            elif t == ">":
                stdout = token[i + 1]
                append = False
                i += 1
            
            elif t == ">>":
                stdout = token[i + 1]
                append = True
                i += 1
            
            else:
                current.append(t)

            i += 1

        if current:
            commands.append((current[0].lower(), current[1:]))
        
        if len(commands) > 1:
            Executor.execute_pipeline(commands, stdin=stdin, stdout=stdout, append=append)
        
        else:
            command, args = commands[0]
            command = command.lower()

            Executor.execute_redirection(command, args, stdin=stdin, stdout=stdout,append=append)

        return

    command = token[0].lower()
    args = token[1:]

    if config.DEBUG == True:
        print(f"\n======== [ Parser ] ========")
        print(f"Token   : {token}")
        print(f"Command : {command}")
        print(f"Args    : {args}")
        print(f"------------------------------")

    cmd = Command(user_input, token, command, args)
    cmd.execute_commands()
