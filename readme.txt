Oprogramowanie napisane w Python generujące stronę sklepową do wkleje nia do Shopify.
Do prawidłowego działania potrzeba:
- [data].csv: specyfikacja produktu w postaci [feature];"[values]"
- plików konfiguracyjnych w katalogu conf
- plików źródłowych w katalogu data:
1. Plik specyfikacji
2. Plik opisu

Program uruchamiamy komendą:
python3 gs.py [liczba_naglowkowa] [nazwa pliku specyfikacji] [nazwa pliku opisu]

Oprogramowanie zadziała bez 3 parametru, ale wygeneruje czystą specyfikację, bez .css, aby to obejść, wystarczy stworzyć pusty plik opisuspecyfikacji
Core softu wykonuje następujące działania:
Wczytaj data.csv do listy data
Obrób listę data:
Przejezdzamy listę data, wykonując następujące działania:
1. Jeśli w linijce jest średnik to wszystko przed średnikiem jest [feature], zatem tworzymy kolejny [feature]
2. J§eśli w linijce jest średnik po którym następuje cudzysłow, to wszystko po cudzysłowie jest [value] do ostatniego ficzeru, po której następuje <br>
3. Jeśli w linijce jst średnik, a nie ma po nim cudzysłowiu to wszystko po cudzysłowiu jest [value] do ostatniego [feature], po której NIE dajemy <br>
4. J§eśli w linijce nie ma średnika to sprawdzamy czy na końcu jest cudzysłow; jeśli nie ma to dajemy <br>, jeśli jest - to nie dajemy; jest to [value] do ostatniego [feature].
Potem dokleja zawartość header.tpl i footer.tpl
Oprogramowanie generuje nagłowek z pierwszych [liczba_naglowkowa] linijek 
Następnie oprogramowanie obrabia plik [opis.html], usuwając linijki z toRemove.tpl, po ostatnim </style> wstawia zawartość header2.tpl.
Ostatnią rzeczą jaką soft robi to złączenie wszystkiego w plik [opis]_final.html.
Pliki tymczasowe nie są czyszczone.
Do zrobienia jest jeszcze uzycie hidden.tpl, które za zadanie ma nie wyświetlac linijek specyfikacji, które mają linijki jak w hidden.tpl lub puste value.