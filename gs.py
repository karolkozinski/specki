import csv
import sys
import os
import io
import datetime
import re



DATA_DIR = "data" 
CONF_DIR = "conf"



def list_directories(path):
    try:
        directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return directories if directories else False  # Jeśli brak katalogów, zwracamy False
    except FileNotFoundError:
        print(f"Ścieżka '{path}' nie istnieje.")
        return False

def log(message):
    # Pobieranie aktualnej daty i godziny
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    log_message = f"{timestamp} >> {message}"

    # Wypisanie komunikatu na konsolę
    print(f"[INFO] {message}")

    # Dopisanie komunikatu do pliku log.txt
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")

    

def load_csv(filename):
    #Wczytuje plik CSV i usuwa ewentualny BOM.
    path = os.path.join(DATA_DIR, filename)
    log(f"Wczytywanie pliku CSV: {path}")

    with open(path, newline='', encoding='utf-8') as file:
        lines = file.readlines()

    if lines and lines[0].startswith("\ufeff"):
        lines[0] = lines[0][1:]

    return list(csv.reader(lines, delimiter=';'))

def process_data(data, omitted_lines):
    #Przetwarza dane z pliku CSV, tworząc strukturę specyfikacji.
    log("Przetwarzanie danych CSV")
    result = {}

    for row in data[omitted_lines:]:
        if len(row) < 2:
            continue

        feature, value = row[0].strip(), row[1].strip().strip('"')

        if feature:
            if feature not in result:
                result[feature] = value
            else:
                result[feature] += "<br>" + value
        else:
            if feature in result:
                result[feature] += "<br>" + value

    return result

def load_template(filename):
    #Wczytuje plik konfiguracyjny (TPL).
    path = os.path.join(CONF_DIR, filename)
    log(f"Wczytywanie szablonu: {path}")

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        log(f"UWAGA: Plik {filename} nie istnieje.")
        return ""

def extract_header_text(csv_filename, omitted_lines):
    #Generuje nagłówek H1 na podstawie pierwszych linii pliku CSV.
    log("Generowanie nagłowka H1 z pliku CSV")
    path = os.path.join(DATA_DIR, csv_filename)

    try:
        with open(path, newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file, delimiter=';'))
            header_lines = [row[0].strip().strip('"') for row in reader[:omitted_lines] if row]

            if header_lines:
                return '<h1 class="naglowek">\n  ' + "<br>\n  ".join(header_lines) + "\n</h1>\n"
    except FileNotFoundError:
        log(f"UWAGA: Plik {csv_filename} nie istnieje. Pomijanie nagłówka.")

    return ""

def insert_style_and_h1(html_filename, style_content, header_text):
    #Wstawia zawartość style.tpl i nagłówek H1 po </style> w pliku HTML.
    log(f"Edytowanie pliku HTML: {html_filename}")

    path = os.path.join(DATA_DIR, html_filename)

    try:
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        log(f"UWAGA: Plik {html_filename} nie istnieje. Pomijanie operacji.")
        return

    pos = html_content.rfind("</style>")
    if pos != -1:
        updated_html = html_content[:pos+8] + "\n" + style_content + "\n" + header_text + "\n" + html_content[pos+8:]
    else:
        updated_html = html_content + "\n" + style_content + "\n" + header_text  

    with open(path, 'w', encoding='utf-8') as file:
        file.write(updated_html)

    log(f"Zaktualizowano plik: {html_filename}")

def save_to_file(output_filename, data):
    #Zapisuje przetworzone dane do pliku HTML.
    log(f"Zapisywanie pliku wynikowego: {output_filename}")

    header = load_template("header.tpl")
    footer = load_template("footer.tpl")

    path = os.path.join(DATA_DIR, output_filename)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(header + "\n")

        for feature, value in data.items():
            formatted_value = value.replace("\n", "<br>")
            file.write(f'<div class="spec_line">\n  <div class="feature_spec">{feature}</div>\n  <div class="value_spec">{formatted_value}</div>\n</div>\n')

        file.write(footer + "\n")

def filter_file(input_filename, output_filename, remove_list_filename):
    #Filtruje linie w pliku HTML na podstawie toRemove.tpl.
    log(f"Filtrowanie pliku: {input_filename}")

    input_path = os.path.join(DATA_DIR, input_filename)
    output_path = os.path.join(DATA_DIR, output_filename)
    remove_list_path = os.path.join(CONF_DIR, remove_list_filename)

    try:
        with open(remove_list_path, 'r', encoding='utf-8') as remove_file:
            remove_lines = [line.strip() for line in remove_file.readlines()]
    except FileNotFoundError:
        log(f"UWAGA: Plik {remove_list_filename} nie istnieje. Pomijanie filtrowania.")
        return

    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    filtered_lines = [line for line in lines if not any(remove_text in line for remove_text in remove_lines)]

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

    log(f"Zapisano przefiltrowany plik: {output_filename}")

def merge_html_files(description_file, specs_file, final_output_file):
    #Łączy plik opisu i specyfikacji w finalny plik HTML.S
    log(f"Laczenie plików: {description_file} + {specs_file} → {final_output_file}")

    desc_path = os.path.join(DATA_DIR, description_file)
    specs_path = os.path.join(DATA_DIR, specs_file)
    final_path = os.path.join(DATA_DIR, final_output_file)

    try:
        with open(desc_path, 'r', encoding='utf-8') as desc_file:
            description_content = desc_file.read()
    except FileNotFoundError:
        log(f"UWAGA: Plik {description_file} nie istnieje. Pomijanie laczenia.")
        return

    try:
        with open(specs_path, 'r', encoding='utf-8') as specs_file:
            specs_content = specs_file.read()
    except FileNotFoundError:
        log(f"UWAGA: Plik {specs_file} nie istnieje. Pomijanie laczenia.")
        return

    with open(final_path, 'w', encoding='utf-8') as final_file:
        final_file.write(description_content + "\n" + specs_content)

    log(f"Wygenerowano plik finalny: {final_output_file}")

def find_single_file(directory, extension):
    """Skanuje katalog w poszukiwaniu plików o podanym rozszerzeniu.
    
    Zwraca nazwę pliku bez rozszerzenia, jeśli znaleziono dokładnie jeden plik.
    W przeciwnym razie zwraca False.
    """
    files = [f for f in os.listdir(directory) if f.endswith(extension)]

    if len(files) == 1:
        return os.path.splitext(files[0])[0]  # Zwraca nazwę pliku bez rozszerzenia
    elif extension == ".html" and len(files) == 0:
        with io.open(os.path.join(directory, 'no_desc.html'), 'w', encoding='utf-8') as file:
            file.write('')
        log(f"Stworzono pusty plik opisu, gdyz takowego brakowalo")
        return 'no_desc'
    return False

def remove_temps (filename,second_filename):
    try: 
        os.remove(DATA_DIR + "/" + filename + ".html")
        if second_filename == "no_desc":
           os.remove(DATA_DIR + "/" + second_filename + ".html")
        os.remove(DATA_DIR + "/" + second_filename + "_res.html")
        os.remove(DATA_DIR + "/" + second_filename + "_beforestripping.html")
        log(f"Temporary files deleted.")
    except FileNotFoundError:
        log("Problems with deleting temporary files")

def how_to_use():
    print('Użycie:')
    print('python gs.py [omitted_lines] >> no dir & final file')
    print('python gs.py [omitted_lines] [csv] >> no dir & only spec')
    print('python gs.py >> w przypadku katalogów')

#hidden.py import

def load_hidden_values(filename):
    """Wczytuje wartości do ukrycia z pliku hidden.tpl."""
    path = os.path.join("conf", filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        log(f"UWAGA: Plik {filename} nie istnieje.")
        return set()

def modify_html(input_filename, output_filename, hidden_values):
    """Dodaje klasę 'N' do spec_line, jeśli wartość value_spec jest pusta lub znajduje się w hidden.tpl."""
    global DATA_DIR
    input_path = os.path.join(DATA_DIR, input_filename)
    output_path = os.path.join(DATA_DIR, output_filename)
    
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        log(f"UWAGA: Plik {input_filename} nie istnieje.")
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
    
    log(f"Zapisano zmodyfikowany plik: {output_filename}")




def main(omitted_lines = False, katalog = False):
    if (katalog):
        global DATA_DIR
        temp = DATA_DIR
        DATA_DIR = DATA_DIR + "/" + katalog
    #print(sys.argv)
    if len(sys.argv) >= 4 or omitted_lines == False:
        #if omitted_lines == False:
            #print("Użycie: python gs.py <liczba_pomijanych_linii> [nazwa_pliku_csv] [drugi_plik_html]")
        how_to_use()
        sys.exit(1)
    #else:
    #    omitted_lines = int(sys.argv[1])

    if len(sys.argv) == 2 or katalog:
        filename = find_single_file(DATA_DIR, ".csv")
        if filename == False:
            log ("Nieprawidlowa ilosc plików .csv w " + DATA_DIR)
            return #sys.exit(1)
        second_filename = find_single_file(DATA_DIR, ".html")
        if second_filename == False:
            log ("Nieprawidlowa ilosc plików .html " + DATA_DIR)
            return #sys.exit(1)      
    
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    if len(sys.argv) == 4:
       second_filename = sys.argv[3]
    #print(sys.argv)
    #print (filename)
    data = load_csv(filename + ".csv")
    processed_data = process_data(data, omitted_lines)

    save_to_file(filename + ".html", processed_data)

    if len(sys.argv) == 4 or len(sys.argv) == 2 or katalog:
        #second_filename = sys.argv[3]
        filter_file(second_filename + ".html", second_filename + "_res.html", "toRemove.tpl")

        style_content = load_template("style.tpl")
        header_text = extract_header_text(filename + ".csv", omitted_lines)
        insert_style_and_h1(second_filename + "_res.html", style_content, header_text)

        merge_html_files(second_filename + "_res.html", filename + ".html", second_filename + "_beforestripping.html")

        #hidden.py incorporation
        filename2 = second_filename + "_beforestripping.html"
        output_filename = second_filename + "_shopify.html"
        hidden_values = load_hidden_values("hidden.tpl")
        modify_html(filename2, output_filename, hidden_values)




        remove_temps (filename,second_filename)
        
        if katalog != False:
            #print (temp, katalog, DATA_DIR)
            DATA_DIR=temp






katalogi = list_directories(DATA_DIR)
#print("ąść")
if __name__ == "__main__":
    if katalogi:  # Jeśli lista ma elementy, wykonujemy pętlę dla każdego elementu
        for katalog in katalogi:
            log(f"\nPRZETWARZAM PRODUKT: {katalog}")
            temp = DATA_DIR
            main(2, katalog)
            DATA_DIR = temp
    else:  # Jeśli lista jest pusta lub False, wykonujemy tylko raz
        if len(sys.argv) == 1:
            log ('Brak pomijanych linii.')
            how_to_use()
            sys.exit(1)
        log(f"PRZETWARZAM PRODUKT:")
        main (int(sys.argv[1]), katalogi)