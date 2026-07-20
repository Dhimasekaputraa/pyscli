from commands import Command
from prompt import get_prompt, parse_and_execute
   
def main():
    while True:
        try:
            user_input = input(get_prompt())

            if not user_input.strip():
                continue

            parse_and_execute(user_input)
            
        except ValueError as e:
            print(f"Syntax error: {e}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            Command.exit_shell()

if __name__ == "__main__":
    main()