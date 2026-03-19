import json
import re
from collections import defaultdict
 
def load_us_to_uk():
    with open("dictionary/us_to_uk_dictionary.json", "r", encoding="utf-8") as f:
        return json.load(f)
 
def convert_to_uk_english(text, us_to_uk):
    for us, uk in us_to_uk.items():
        text = re.sub(rf"\b{us}\b", uk, text, flags=re.IGNORECASE)
    return text
 
def is_sentence_correct(user_input, corrected_text):
    return user_input.strip() == corrected_text.strip()