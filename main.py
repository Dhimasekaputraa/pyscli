def main():
    while True:
        try:
            user_input = input(f"user@myshell:~$ ").lower()

            if not user_input.strip():
                continue

            # Dev only : to show what's user input after the cleaning
            # print(f"Raw input: '{user_input}'\nInput after cleaning: '{user_input.strip()}'")

            if user_input.strip() == "exit":
                break

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()