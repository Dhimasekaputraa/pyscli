import os
import subprocess

class Executor:
    @staticmethod
    def _execute_windows(command, args):
        try:
            subprocess.run(
                [command]+args,
                shell=True 
            )
        except FileNotFoundError:
            print(f"{command}: not found")
        except subprocess.CalledProcessError:
            print(f"error executing command")
        except Exception as e:
            print(f"error: {e}")

    @staticmethod
    def _execute_posix(command, args):
        try:
            pid = os.fork()
        except OSError as e:
            print(f"fork failed: {e}")
            return
        
        if pid == 0:
            try:
                os.execvp(
                    command, [command] + args
                )
            except FileNotFoundError:
                print(f"{command}: command not Found")
            except Exception as e:
                print(f"execution error: {e}")
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
              print(e)
        
          finally:
            if stdin_file:
                stdin_file.close()

            if stdout_file:
                stdout_file.close()

        else:
            try:
                pid = os.fork()
                if pid == 0:

                    if stdin:
                        fd = os.open(stdin, os.O_RDONLY)
                        os.dup2(fd, 0) 
                        os.close(fd)
                    
                    if stdout:
                        if append: flags = (os.O_WRONLY | os.O_CREAT | os.O_APPEND)

                        else:
                            flags = (os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    
                        fd = os.open(stdout, flags, 0o644)
                        os.dup2(fd, 1)
                        os.close(fd)

                    try:
                        os.execvp(command, [command]+args)
                    except Exception as e:
                        print(e)
                        os._exit(1)

                else:
                    os.waitpid(pid, 0)
            except Exception as e:
                print(f"Redirection error: {e}")
    
    @staticmethod
    def execute_pipeline(commands, stdin=None, stdout=None, append=False):
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

            for i in range(num_commands):
                command, args = commands[i]
                pid = os.fork()
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
                        print(e)
                        os._exit(1)
        
                else:
                    pids.append(pid)

            for r, w in pipes:
                os.close(r)
                os.close(w)
            for pid in pids:
                os.waitpid(pid, 0)