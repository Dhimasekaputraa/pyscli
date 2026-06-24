import os
import sys
import subprocess

class Executor:
    @staticmethod
    def _execute_windows(command, args):
        try:
            subprocess.run([command] + args, check=True)
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
                os.execvp(command, [command] + args)
            except Exception as e:
                print(f"execution error: {e}")
            os._exit(1)
        else:
            os.waitpid(pid, 0)

    @staticmethod
    def execute_external(command, args):
        if os.name == "nt":
            Executor._execute_windows(command, args)
        else:
            Executor._execute_posix(command, args)

    @staticmethod
    def execute_redirection_out(command, args, filename):
        if os.name == "nt":
            try:
                with open(filename, "w") as f:
                    subprocess.run([command] + args, stdout=f, check=True)
            except Exception as e:
                print(f"Redirection error: {e}")
        else:
            try:
                pid = os.fork()
                if pid == 0:
                    fd_file = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    os.dup2(fd_file, 1)
                    os.close(fd_file)
                    os.execvp(command, [command] + args)
                else:
                    os.waitpid(pid, 0)
            except Exception as e:
                print(f"Redirection error: {e}")

    @staticmethod
    def execute_redirection_in(command, args, filename):
        if os.name == "nt":
            try:
                with open(filename, "r") as f:
                    subprocess.run([command] + args, stdin=f, check=True)
            except Exception as e:
                print(f"Input Redirection error: {e}")
        else:
            try:
                pid = os.fork()
                if pid == 0:
                    fd_file = os.open(filename, os.O_RDONLY)
                    os.dup2(fd_file, 0)
                    os.close(fd_file)
                    os.execvp(command, [command] + args)
                else:
                    os.waitpid(pid, 0)
            except Exception as e:
                print(f"Input Redirection error: {e}")

    @staticmethod
    def execute_pipeline(commands):
        if os.name == "nt":
            pipeline_str = " | ".join([f"{cmd} {' '.join(args)}" for cmd, args in commands])
            subprocess.run(pipeline_str, shell=True)
        else:
            num_commands = len(commands)
            pipes = [os.pipe() for _ in range(num_commands - 1)]
            pids = []

            for i in range(num_commands):
                command, args = commands[i]
                pid = os.fork()
                if pid == 0:
                    if i > 0: os.dup2(pipes[i-1][0], 0)
                    if i < num_commands - 1: os.dup2(pipes[i][1], 1)
                    for r, w in pipes:
                        os.close(r)
                        os.close(w)
                    os.execvp(command, [command] + args)
                else:
                    pids.append(pid)

            for r, w in pipes:
                os.close(r)
                os.close(w)
            for pid in pids:
                os.waitpid(pid, 0)