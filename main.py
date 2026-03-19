from assistant import process_input
 
def run_assistant():
    print("Grammar & Spelling Corrector (Type 'exit' to quit)\n")
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Assistant: Session ended.")
            break
 
        if user_input.lower().startswith("rephrase:"):
            mode = "rephrase"
            actual_input = user_input[len("rephrase:"):].strip()
        else:
            mode = "grammar and spelling correction"
            actual_input = user_input
 
        result = process_input(actual_input, mode=mode)
        print(f"Assistant: {result}")
 
if __name__ == "__main__":
    run_assistant()