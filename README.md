# Teoria kompilacji i kompilatory
## Interpreter pythona w pythonie



Interpreter pythona często rozumiany jest jako:
  - REPL (Read-Evaluate-Print-Loop) - czyli interaktywne środowisko programowania, wiersz poleceń powłoki
  - wykonawca programów napisanych w pythonie od początku do końca 
  
Python jest dynamicznie typowanym językiem interpretowanym, ale tak jak większość języków interpretowanych zawiera krok kompilacji. Krok ten jednak wykonuje znacząco mniej pracy i zawiera relatywnie mniej informacji o programie niż w przypadku języków kompilowanych takich jak C.
W tym projekcie interpreter pythona będzie odpowiedzialny za ostatni etap w procesie wykonywania programów w pythonie. Na wejściu będzie otrzymywał kod źródłowy, przekształcony wcześniej przez lekser, parser i kompilator do struktury obiektów (*code objects*) zawierających instrukcje (*bytecode*) możliwe do zrozumienia przez interpreter. Rolą interpretera będzie wykonanie tych instrukcji.

Zalety:
 - łatwość implementacji i zrozumienia kodu, dzięki użyciu języka wysokiego poziomu 
 - możliwość implementcji tylko interpretera, bez angażowania innych elementów analizy programu

Wady:
- szybkość (oryginalny interpreter napisany w C jest bardzo dobrze zoptymalizowany)

### Zasada działania interpretera 

- interpreter jest maszyną wirtualną (*virtual machine*), reprezentowaną przez maszynę stosową (*stack machine*) - wykonuje operacje manipulując stosami, dzięki czemu w łatwy sposób można śledzić jego stan (w przeciwieństwie do maszyny rejestrowej (*register machine*), która pisze i czyta z konkretnych miejsc w pamięci)
- obiekt interpretera zawiera stos, reprezentowany przez listę, oraz metody opisujące jak wykonać poszczególne instrukcje, operując na tym stosie.
- interpreter jest odpowiedzialny za wykonanie instrukcji, które dostał na wejściu
- interpreter dostaje na wejściu *code objec*, który jest zbiorem instrukcji (i dodatkowych niezbędnych informacji) zawierającym się w obiektach (*code objects*), wygenerowanych we wcześniejszym kroku przez kompilator. *Bytecode* jest pośrednią reprezentacją kodu w Pythonie - reprezentuje napisany kod źródłowy w sposób możliwy do zrozumienia przez interpreter.

Wejście interpretera, czyli *code object* składa się z dwóch części:
- listy instrukcji (*bytecode*), złożonej z par (nazwa_instrukcji,arg_index) 
- listy stałych (argumentów funkcji) wywoływanych przez konkretne instrukcje (jeśli takowe argumenty są potrzebne).
Można je przedstawić przy pomocy słownika:
```
program_do_wykonania = {
  "instrukcje": [("nazwa_instrukcji", 0), # pierwszy argument
                 ("nazwa2_instrukcji, None), # instrukcja bezargumentowa
                 ...],
  "argumenty": [arg1, arg2, ...] # dla każdego typu danych osobna lista
}
```
Wykonanie programu, w uproszczeniu, odbywa się przez wywołanie po kolei wszystkich instrukcji, wraz z odpowiednimi argumentami.


#### Funkcje
Każda instrukcja w wejściowym *bytecodzie* musi mieć zapewnioną implementację odpowiedniej funkcji operującej na stosie.
Na przykład dodanie dwóch liczb sprowadza się do trzech instrukcji:
1. Wprowadzenie stałych - umieszczenie liczb na stosie
2. Dodanie dwóch stałych - ściągnięcie dwóch liczb ze stosu, dodanie ich i umieszczenie wyniku z powrotem na stosie
3. Wypisanie wyniku - ściągnięcie ze stosu i wypisanie liczby

#### Zmienne
W szczególności, do wprowadzenia zmiennych, w obiekcie wejściowym potrzebna jest dodatkowa lista zmiennych i funkcja uzupełniająca słownik wiążący nazwy zmiennych z ich wartościami. Interpreter wie z której listy w danym momencie ma skorzystać na podsatwie rodzaju wykonywanej instrukcji. Do mapowania instrukcji na odpowiedni argument służy funkcja parsująca, która każdą instrukcję kwalifikuje do odpowiedniej listy argumentów.

#### Wyrażenia warunkowe i pętle
Do ewaluowania wyrażeń warunkowych i wykonywania pętli potrzebne są instrukcje skoków (warunkowych i bezwarunkowych) oraz operatory porównywania posiadające swoje implementacje funkcji operujących na stosie. Instrukcje skoków jako argument przyjmują indeks instrukcji do której ma ''skoczyć'' interpreter, tzw. *jump target*.
TODO fill

### Frames
Ramka jest pewnym kontekstem, zbiorem informacji dla fragmentu kodu, zawierającym własny stos danych. Każdemu wywołaniu funkcji, każdej definicji klasy i każdemu modułowi towarzyszy jedna tworzona w locie ramka, więc z każdą ramką powiązany jest jeden *code object*, ale jeden *code object* może zawierać wiele ramek. Ramki żyją na stosie wywołań (*call stack*), a po powrocie z funkcji są niszczone (zdejmowane ze stosu). 
Szczególnym przypadkiem jest instrukcja zwracająca, która powoduje przekazanie wartości między ramkami:
1. Zdjęcie ze stosu danych (*data stack*) wartości odpowiadającej ramce będącej na szczycie stosu wywołań
2. Zdjęcie tej ramki ze stosu wywołań
3. Dodanie wcześniej zdjętej wartości na stos danych kolejnej ramki


### Implementacja

#### Implementacja cz.1
W pierwszej części implementacji stworzyliśmy szkielet systemu składający się z 3 klas:
  - Virtual Machine - odpowiedzialna za zarządzanie działaniem całego interpretera, którego w trakcie działania programu tworzona jest jedna instancja. Przechowuje stos wywołań (ramek) oraz wartośći zwracane i przekazywane między ramkami. Mapuje instrukcje *bytecodu* na funkcje operujące na tych stosach.  
  - Frame - zarządzająca pojedynczą ramką danych - każda instancja klasy ma jeden *code object*, swój stos danych, przestrzenie nazw (lokalne, globalne i wbudowane), referencje do ramki wywołującej i ostatnią wykonaną instrukcję.
  - Function - sterowanie tworzeniem nowych ramek (przy wywoływaniu funkcji). Zamiast normalnych funkcji Pythona
  
#### Implementacja cz.2
W drugiej części przygotowany wcześniej szkielet programu został wypełniony. Dodatkowo zostały zaimplementowane podstawowe instrukcje (dodawanie, odejmowanie, mnożenie, dzielenie, pobieranie zmiennych, stałych itp.). W aktualnej wersji interpreter jest w stanie przyjąć wcześniej skompilowany kod i przeprowadzić na nim swoje operacje. 

TODO
-możliwości kompilacji - compile i obj.__code__
-python 3.5
-The bytecodes that manipulate the stack always operate on the current frame's data stack

Struktura *prawdziwego bytecodu* w zasadzie nie różni sie od przedstawionej, z dokładnością do używania jednego bajta pamięci zamiast długich nazw opisowych. Python udostępnia wiele swoich elementów podczas działania programu takich jak:
 - func_name.\_\_code__ - *code object* powiązany z funkcją
 - func_name.\_\_code__.co_code - *bytecode*
 - getattr(self, instruction) - w celu dynamicznego sprawdzania nazw kolejnych metod żeby uniknąć potwornego ifa 
 - dis.dis(func_name) - przedstawia kod maszynowy (tu *bytecod*) w formie czytelnej dla ludzi
 
 
#### Implementacja cz.3
W trzeciej części implementacji dodaliśmy obsługę kolejnych instrukcji, tak że w finalnym projekcie mamy dostep do podstawowcyh operacji matematycznych (mnożenie, dzielenie, modulo, dodawanie, odejmowanie), operatorów logicznych (OR i AND), operatorów porównania (większe od, większe bądź równe, równe, nierówne, mniejsze, mniejsze bądź równe), do instrukcji warunkowych if..else oraz pętli for.

