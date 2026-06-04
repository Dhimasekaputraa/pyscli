import os
from commands import Command
   
def main():
    while True:
        try:
            current_path = "" + os.path.basename(os.getcwd())
            user_input = input(f"user@myshell | {current_path}$ ")

            if not user_input.strip():
                continue

            token = user_input.strip().split()
            command = token[0].lower()
            args = token[1:]

            # dev only : to show what's inside token and which is command or args
            # print(f"Token : {token}\nCommand:{command}, Args:{args}")

            cmd = Command(user_input, token, command, args)
            cmd.execute_commands()

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()
