def load_system_prompt():
    with open("prompt.txt","r",encoding="utf-8") as f:
        return f.read()