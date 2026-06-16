import os
import subprocess

class Executor:
    @staticmethod
    def execute_external(command, args):
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