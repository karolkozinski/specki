Oprogramowanie napisane w Python generujące stronę sklepową do wkleje nia do Shopify.
Do prawidłowego działania potrzeba:
- [data].csv: specyfikacja produktu w postaci [feature];"[values]"
- plików konfiguracyjnych w katalogu conf
- plików źródłowych w katalogu data:
1. Plik specyfikacji
2. Plik opisu

Użycie:
python gs.py [omitted_lines] >> no dir & final file
python gs.py [omitted_lines] [csv] >> no dir & only spec
python gs.py >> gs >> when dirs, header needs to be a single line

Właściwie użycie (po skompilowaniu) to uruchomienie pliku gs.exe z odpowiednio sformatowanymi i wypełnionymi katalogami w /data oraz /hidden i /conf.

Core softu wykonuje następujące działania:
Wczytaj data.csv do listy data
Obrób listę data:
Przejezdzamy listę data, wykonując następujące działania:
1. Jeśli w linijce jest średnik to wszystko przed średnikiem jest [feature], zatem tworzymy kolejny [feature]
2. J§eśli w linijce jest średnik po którym następuje cudzysłow, to wszystko po cudzysłowie jest [value] do ostatniego ficzeru, po której następuje <br>
3. Jeśli w linijce jst średnik, a nie ma po nim cudzysłowiu to wszystko po cudzysłowiu jest [value] do ostatniego [feature], po której NIE dajemy <br>
4. Jeśli w linijce nie ma średnika to sprawdzamy czy na końcu jest cudzysłow; jeśli nie ma to dajemy <br>, jeśli jest - to nie dajemy; jest to [value] do ostatniego [feature].
Potem dokleja zawartość header.tpl i footer.tpl
Oprogramowanie generuje nagłowek z pierwszych [liczba_naglowkowa] linijek 
Następnie oprogramowanie obrabia plik [opis.html], usuwając linijki z toRemove.tpl, po ostatnim </style> wstawia zawartość header2.tpl.
Ostatnią rzeczą jaką soft robi to złączenie wszystkiego w plik [opis]_final.html.
Pliki tymczasowe są czyszczone.
hidden.py [nazwa_pliku_html_bez_rozszerzenia] do kazdej klasy spec_line dodaje klasę N jeśli feature jest w hidden.tpl lub jest puste.