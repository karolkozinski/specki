import os
import re
import sys

def load_hidden_values(filename):
    """Wczytuje wartości do ukrycia z pliku hidden.tpl."""
    path = os.path.join("conf", filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"UWAGA: Plik {filename} nie istnieje.")
        return set()

def modify_html(input_filename, output_filename, hidden_values):
    """Dodaje klasę 'N' do spec_line, jeśli wartość value_spec jest pusta lub znajduje się w hidden.tpl."""
    input_path = os.path.join("data", input_filename)
    output_path = os.path.join("data", output_filename)
    
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"UWAGA: Plik {input_filename} nie istnieje.")
        return
    
    def replace_match(match):
        spec_line, feature, value = match.groups()
        clean_value = re.sub(r"<br>.*", "", value).strip()  # Pobiera pierwszą linię wartości
        
        if not clean_value or clean_value in hidden_values:
            return spec_line.replace("spec_line", "spec_line N")
        return spec_line
    
    updated_html = re.sub(
        r"(<div class=\"spec_line\">\s*<div class=\"feature_spec\">(.*?)</div>\s*<div class=\"value_spec\">(.*?)</div>\s*</div>)",
        replace_match,
        html_content,
        flags=re.DOTALL
    )
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(updated_html)
    
    print(f"Zapisano zmodyfikowany plik: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python skrypt.py <nazwa_pliku_bez_rozszerzenia>")
        sys.exit(1)
    
    filename = sys.argv[1] + ".html"
    output_filename = sys.argv[1] + "_mod.html"
    hidden_values = load_hidden_values("hidden.tpl")
    modify_html(filename, output_filename, hidden_values)