import os
import subprocess
import config

class Executor:
    @staticmethod
    def _execute_windows(command, args):
        try:
            subprocess.run(
                [command]+args,
                shell=True 
            )
        except FileNotFoundError:
            print(f"{config.RED}{command}: not found")
        except subprocess.CalledProcessError:
            print(f"{config.RED}error executing command")
        except Exception as e:
            print(f"{config.RED}error: {e}")

    @staticmethod
    def _execute_posix(command, args):
        try:
            pid = os.fork()
        except OSError as e:
            print(f"{config.RED}fork failed: {e}")
            return
        
        if config.DEBUG and pid != 0:
            print("\n=== [ PID Information ] ===")
            print(f"Parent PID : {os.getpid()}")
            print(f"Child PID  : {pid}")
            print("---------------------------\n")
        
        if pid == 0:
            try:
                os.execvp(
                    command, [command] + args
                )
            except FileNotFoundError:
                print(f"{config.RED}{command}: command not Found")
            except Exception as e:
                print(f"{config.RED}execution error: {e}")
            os._exit(1)

        else:
            os.waitpid(pid, 0)

    @staticmethod
    def execute_external(command, args):

        if os.name == "nt":
            Executor._execute_windows(
                command, args
            )
        else:
            Executor._execute_posix(
                command, args
            )

    @staticmethod
    def execute_redirection(command, args, stdin=None, stdout=None, append=False):
        if config.DEBUG == True:
            print("\n=== [ Redirection ] ===")
            print(f"Command  : {command}")
            print(f"Args     : {args}")
            print(f"Stdin\t: {stdin}")
            print(f"Stdout\t: {stdout}")
            print(f"Append\t: {append}")
            print("-----------------------\n")
        if os.name == "nt":
          stdin_file = None
          stdout_file = None
          try:
            if stdin:
                stdin_file = open(stdin, "r")
            if stdout:
                mode = "a" if append else "w"
                stdout_file = open(stdout, mode)
            
            subprocess.run([command] + args,
                        stdin=stdin_file,
                        stdout=stdout_file,
                        shell=True)
            
          except Exception as e:
              print(f"{config.RED}{e}")
        
          finally:
            if stdin_file:
                stdin_file.close()

            if stdout_file:
                stdout_file.close()

        else:
            try:
                pid = os.fork()

                if config.DEBUG and pid != 0:
                    print("=== [ PID Information ] ===")
                    print(f"Parent PID : {os.getpid()}")
                    print(f"Child PID  : {pid}")
                    print("---------------------------\n")

                if pid == 0:

                    if stdin:
                        fd = os.open(stdin, os.O_RDONLY)
                        os.dup2(fd, 0)
                        if config.DEBUG:
                            print("=== [ File Descriptor ] ===")
                            print(f"Input File  : {stdin}")
                            print(f"FD          : {fd}")
                            print(f"Redirect    : {stdin} (FD {fd}) -> STDIN (FD 0)")
                            print("---------------------------\n")
                        os.close(fd)
                    
                    if stdout:
                        if append: flags = (os.O_WRONLY | os.O_CREAT | os.O_APPEND)

                        else:
                            flags = (os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    
                        fd = os.open(stdout, flags, 0o644)
                        if config.DEBUG:
                            print("=== [ File Descriptor ] ===")
                            print(f"Output File : {stdout}")
                            print(f"Append      : {append}")
                            print(f"FD          : {fd}")
                            print(f"Redirect    : STDOUT (FD 1) -> {stdout} (FD {fd})")
                            print("---------------------------\n")
                        os.dup2(fd, 1)
                        os.close(fd)

                    try:
                        os.execvp(command, [command]+args)
                    except Exception as e:
                        print(f"{config.RED}{e}")
                        os._exit(1)

                else:
                    os.waitpid(pid, 0)
            except Exception as e:
                print(f"{config.RED}Redirection error: {e}")
    
    @staticmethod
    def execute_pipeline(commands, stdin=None, stdout=None, append=False):
        if config.DEBUG == True:
            print("\n=== [ PIPELINE ] ===")
            for i, (cmd, args) in enumerate(commands, start=1):
                print(f"[{i}]")
                print(f"Cmd\t: {cmd}")
                print(f"Args\t: {args}")
                print("---------------------")
            print(f"Stdin\t: {stdin}")
            print(f"Stdout\t: {stdout}")
            print(f"Append\t: {append}")
            print("-----------------------\n")
        if os.name == "nt":
            stdin_file = None
            stdout_file = None
            pipeline_str = " | ".join([f"{cmd} {' '.join(args)}" for cmd, args in commands])
            if stdin:
                stdin_file = open(stdin, "r")
            if stdout:
                mode = "a" if append else "w"
                stdout_file = open(stdout, mode)
            subprocess.run(pipeline_str, shell=True, stdin=stdin_file, stdout=stdout_file)
        else:
            num_commands = len(commands)
            pipes = [os.pipe() for _ in range(num_commands - 1)]
            pids = []

            if config.DEBUG:
                print("=== [PID Information] ===")
                print(f"Parent PID : {os.getpid()}")
                print("---------------------------")

            for i in range(num_commands):
                command, args = commands[i]
                pid = os.fork()

                if config.DEBUG and pid != 0:
                    print(f"[{i+1}]")
                    print(f"Command    : {command}")
                    print(f"Child PID  : {pid}")
                    print("---------------------------")

                if pid == 0:
                    if i == 0 and stdin:
                        fd = os.open(stdin, os.O_RDONLY)
                        os.dup2(fd, 0)
                        os.close(fd)
                    if i > 0: os.dup2(pipes[i-1][0], 0)
                    if i < num_commands - 1: os.dup2(pipes[i][1], 1)
                    if i == num_commands - 1 and stdout:
                        if append:
                            flags = (os.O_WRONLY | os.O_CREAT | os.O_APPEND)
                        else:
                            flags = (os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                        fd = os.open(stdout, flags, 0o644)
                        os.dup2(fd, 1)
                        os.close(fd)
                    for r, w in pipes:
                        os.close(r)
                        os.close(w)
                    try:
                        os.execvp(command, [command] + args)
                    except Exception as e:
                        print(f"{config.RED}{e}")
                        os._exit(1)
        
                else:
                    pids.append(pid)
            
            if config.DEBUG:
                print("\n=== [ Pipe Descriptor ] ===")
                for pipe_no, (r, w) in enumerate(pipes, start=1):
                    print(f"Pipe {pipe_no}")
                    print(f"Read FD  : {r}")
                    print(f"Write FD : {w}")
                print("---------------------------") 

            for r, w in pipes:
                os.close(r)
                os.close(w)
            for pid in pids:
                os.waitpid(pid, 0)