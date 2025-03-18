# Automatic Extraction

### Wprowadzenie
Automatic Extraction to narzędzie dla rzeczoznawców majątkowych do całkowitej automatyzacji zczytywania danych o nieruchomościach z aktów notarialnych. Obsługa jest prosta - Wystarczy włożyć akty do folderu input a po zakończeniu działania program wyśle wyniki do folderu output.

### Skąd na to potrzeba?
W procesie oceniania wartości nieruchomości często najdłuższym krokiem jest wydobycie podstawowych danych o cenie, lokalizacji i wymiarach danej działki. Jeśli nieruchomości nie ma w żadnej bazie, jest to zazwyczaj robione w sposób manualny - dane są odczytywane po kolei z aktów notarialnych co zajmuje często całe tygodnie. Zważając na prostą i przewidywalną strukturę tych aktów widać w tym potencjał na automatyzację.

### Jak działa Automatic Extraction?
Najpierw akty są odczytywane lokalnie za pomocą narzędzia tesseract OCR, następnie w powstałym tekście program szuka słów kluczy za pomocą wyrażeń regularnych i wyniki zapisuje w pliku .xlsx

### Jakie pola są zawarte w wyniku?
Na razie program obsługuje cenę całkowitą, powierzchnię całkowitą, numer działki, datę transakcji, numer repozytorium i obręb.

