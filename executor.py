import os
import subprocess

class Executor:
    @staticmethod
    def _execute_windows(command, args):
        try:
            subprocess.run(
                [command]+args,
                check=True 
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