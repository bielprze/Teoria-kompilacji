# Teoria kompilacji i kompilatory
## Interpreter pythona w pythonie

Interpreter pythona często rozumiany jest jako:
  - REPL (Read-Evaluate-Print-Loop) - czyli interaktywne środowisko programowania, wiersz poleceń powłoki
  - wykonawca programów napisanych w pythonie od początku do końca 
  
W tym projekcie interpreter pythona będzie odpowiedzialny za ostatni etap w procesie wykonywania programów w pythonie. Na wejściu będzie otrzymywał kod źródłowy, przekształcony wcześniej prze lekser, parser i kompilator do struktury obiektów (*code obiects*) zawierających instrukcje (*bytecode*) możliwe do zrozumienia przez interpreter. Rolą interpretera będzie wykonanie tych instrukcji.

Zalety:
 - łatwość implementacji 
 - łatwość zrozumienia, dzięki użyciu języka wysokiego poziomu 

Wady:
- szybkość (oryginalny interpreter napisany w C jest bardzo dobrze zoptymalizowany)

Założenia:
- interpreter jest maszyną stosową (*stack machine*) - wykonuje operacje manipulując stosami (w przeciwieństwie do maszyny rejestrowej)
- interpreter dostaje na wejściu *bytecode*, który jest zbiorem instrukcji zawierającym się w obiektach (*code obiects*) wygenerowanych we wcześniejszym kroku przez kompilator
- interpreter jest odpowiedzialny za wykonanie instrukcji, które dostał

## Implementacja cz.1
W pierwszej części implementacji stworzyliśmy szkielet systemu składający się z 3 klas:
  - Virtual Machine - odpowiedzialna za zarządzanie działaniem całego interpretera. Zostały w niej zaimplementowane metody do obsługi stosu ramek oraz stosu danych. 
  - Frame - zarządzająca pojedynczą ramką danych
  - Function - sterowanie ramkami tworzonymi przez wywołanie funkcji
  
## Implementacja cz.2
W drugiej części przygotowany wcześniej szkielet programu został wypełniony. Dodatkowo zostały zaimplementowane podstawowe instrukcje (dodawanie, odejmowanie, mnożenie, dzielenie, pobieranie zmiennych, stałych itp.). W aktualnej wersji interpreter jest w stanie przyjąć wcześniej skompilowany kod i przeprowadzić na nim swoje operacje. 
