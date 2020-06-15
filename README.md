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

Jak działa interpreter Pythona:
- interpreter jest maszyną wirtualną (*virtual machine*), reprezentowaną przez maszynę stosową (*stack machine*) - wykonuje operacje manipulując stosami, dzięki czemu w łatwy sposób można śledzić jego stan (w przeciwieństwie do maszyny rejestrowej (*register machine*), która pisze i czyta z konkretnych miejsc w pamięci)
- interpreter dostaje na wejściu *bytecode*, który jest zbiorem instrukcji (i dodatkowych niezbędnych informacji) zawierającym się w obiektach (*code objects*), wygenerowanych we wcześniejszym kroku przez kompilator. *Bytecode* jest pośrednią reprezentacją kodu w Pythonie - reprezentuje napisany kod źródłowy w sposób możliwy do zrozumienia przez interpreter.
- interpreter jest odpowiedzialny za wykonanie instrukcji, które dostał na wejściu

Wejście interpretera, czyli *code object* składa się z dwóch części:
- listy instrukcji (*bytecode*)
- listy stałych używanych przez konkretne instrukcje (jeśli takowe są potrzebne)

## Implementacja cz.1
W pierwszej części implementacji stworzyliśmy szkielet systemu składający się z 3 klas:
  - Virtual Machine - odpowiedzialna za zarządzanie działaniem całego interpretera. Zostały w niej zaimplementowane metody do obsługi stosu ramek oraz stosu danych. 
  - Frame - zarządzająca pojedynczą ramką danych
  - Function - sterowanie ramkami tworzonymi przez wywołanie funkcji
  
## Implementacja cz.2
W drugiej części przygotowany wcześniej szkielet programu został wypełniony. Dodatkowo zostały zaimplementowane podstawowe instrukcje (dodawanie, odejmowanie, mnożenie, dzielenie, pobieranie zmiennych, stałych itp.). W aktualnej wersji interpreter jest w stanie przyjąć wcześniej skompilowany kod i przeprowadzić na nim swoje operacje. 
