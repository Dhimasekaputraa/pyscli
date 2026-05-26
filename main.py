# CLI SHELL USING PYTHON

# -- Tokenization
def tokenization(clean_command) :
    tokens = clean_command.split()
    # print(tokens)
    return tokens

# -- MAIN LOOP (REPL)
running = True
while running :
    print("user@device : $ ", end = "") #Temporary, can be upgraded to get username and userdevice info
    # Get the user input
    raw_command = input("")

    # Clean the input form white space
    clean_command = raw_command.strip()
    
    tokenization(clean_command)

    # -- Evaluator (Needs to make it's own function)
    # Blank space condition
    if clean_command == "" :
        continue

    # exit condition
    if clean_command == "exit" :
        running = False