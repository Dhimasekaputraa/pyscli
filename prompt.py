import os
import getpass
import socket
import shlex
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

    return f"{GREEN}{user_info['user']}{RESET} | {BLUE}{user_info['host']}{RESET} : {cwd}$ "

def parse_and_execute(user_input):
    PIPE = "|"
    REDIRECTION_IN = "<"
    REDIRECTION_OUT = ">"

    if PIPE in user_input:
        commands_list = [cmd.strip() for cmd in user_input.split("|")]
        parsed_commands = []
        for cmd_str in commands_list:
            tokens = shlex.split(cmd_str)
            if tokens:
                parsed_commands.append((tokens[0], tokens[1:]))
        
        Executor.execute_pipeline(parsed_commands)
        return

    if REDIRECTION_IN in user_input:
        cmd_part, file_part = user_input.split("<", 1)
        tokens = shlex.split(cmd_part.strip())
        file_tokens = shlex.split(file_part.strip())
        
        if not tokens or not file_tokens:
            print("Syntax error: Invalid redirection syntax.")
            return
            
        command = tokens[0].lower()
        args = tokens[1:]
        filename = file_tokens[0]
        
        Executor.execute_redirection_in(command, args, filename)
        return

    if REDIRECTION_OUT in user_input:
        cmd_part, file_part = user_input.split(">", 1)
        tokens = shlex.split(cmd_part.strip())
        file_tokens = shlex.split(file_part.strip())
        
        if not tokens or not file_tokens:
            print("Syntax error: Invalid redirection syntax.")
            return
            
        command = tokens[0].lower()
        args = tokens[1:]
        filename = file_tokens[0]
        
        Executor.execute_redirection_out(command, args, filename)
        return
    

    token = shlex.split(user_input)
    command = token[0].lower()
    args = token[1:]

    cmd = Command(user_input, token, command, args)
    cmd.execute_commands()