def main():
    while True:
        try:
            user_input = input(f"user@myshell$ ").lower()

            if not user_input.strip():
                continue
                
            if user_input.strip() == "exit":
                break

        except (KeyboardInterrupt, EOFError):
            print("Gunakan 'exit' untuk keluar.")
            continue

if __name__ == "__main__":
    main()
