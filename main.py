import os
from commands import Command
   
def main():
    while True:
        try:
            current_path = "user@myshell:~$ " + os.path.basename(os.getcwd())
            user_input = input(f"{current_path} ")

            if not user_input.strip():
                continue

            token = user_input.strip().split()
            command = token[0].lower()
            args = token[1:]

            cmd = Command(user_input, token, command, args)
            cmd.execute_commands()

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()