from happytransformer import HappyTextToText

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

def fix_punctuation(text):
    result = happy_tt.generate_text(f"grammar: {text}")
    return result.text

text = "merhaba nasılsın ben iyi sen"
fixed_text = fix_punctuation(text)
print(fixed_text) 
