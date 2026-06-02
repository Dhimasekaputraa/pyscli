import sys
import os
import commands
   
def main():
    while True:
        try:
            user_input = input("user@myshell:~$ ")

            if not user_input.strip():
                continue

            token = user_input.strip().split()
            command = token[0].lower()
            args = token[1:]

            cmd = commands.Command(user_input, token, command, args)
            cmd.execute_commands()

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()