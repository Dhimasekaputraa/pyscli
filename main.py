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
            command = token[0].lower()
            args = token[1:]

            cmd = Command(user_input, token, command, args)
            cmd.execute_commands()
        
        except ValueError as e:
            print(f"Syntax error: {e}")

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()