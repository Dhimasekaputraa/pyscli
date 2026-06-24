from commands import Command
from prompt import get_prompt
import shlex
   
def main():
    while True:
        try:
            user_input = input(get_prompt())

            if not user_input.strip():
                continue

            token = shlex.split(user_input)
            command = token[0]
            args = token[1:]

            cmd = Command(user_input, token, command, args)
            cmd.execute_commands()

            if Command.debug == True:
                print("\n----------------------------")
                print(f"[Tokens]  : {cmd.token}")
                print(f"[Command] : {cmd.command}")
                print(f"[Args]    : {cmd.args}")
                print("------------------------------")
        
        except ValueError as e:
            print(f"Syntax error: {e}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            Command.exit_shell()

if __name__ == "__main__":
    main()