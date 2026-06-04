# OSPAN – Operation Span Task

Komputerowa implementacja zadania Operation Span (OSPAN) do pomiaru pojemności pamięci roboczej (Working Memory Capacity). Zbudowana w PsychoPy.

## Opis badania

Badanie mierzy zdolność do jednoczesnego przechowywania i przetwarzania informacji. Uczestnik na przemian:
1. Ocenia równania matematyczne (Prawda / Fałsz)
2. Zapamiętuje litery pojawiające się na ekranie

Na końcu każdej próby wskazuje zapamiętane litery w kolejności ich pojawiania się.

**Struktura badania:**
- Trening: 3 próby (nie wliczane do wyniku)
- Badanie właściwe: 15 prób (rozmiary sekwencji 3–7 liter, losowa kolejność)
- Wynik pamięciowy próby jest liczony tylko jeśli poprawność matematyczna ≥ 85%

## Wymagania

```
psychopy
pyyaml
```

Zalecane środowisko: `conda` lub `venv` z Python 3.10.

```bash
pip install psychopy pyyaml
```

## Uruchomienie

```bash
cd src
python main.py
```

Przed właściwym badaniem pojawi się okno z prośbą o podanie wieku i płci uczestnika. Program przydziela automatycznie unikalny ID.

## Konfiguracja

Wszystkie parametry badania znajdują się w `src/config.yaml`:

| Parametr | Opis |
|---|---|
| `timing.equation_max` | Maks. czas na ocenę równania (s) |
| `timing.letter_max` | Maks. czas wyświetlania litery (s) |
| `timing.blank_min/max` | Zakres losowej przerwy między bodźcami (s) |
| `timing.break_max` | Maks. czas przerwy między próbami (s) |
| `scoring.math_threshold` | Wymagany % poprawności matematycznej |
| `display.fullscreen` | `true` do badania, `false` do testowania |

## Dane wyjściowe

Po zakończeniu badania w folderze `data/` tworzony jest plik CSV:

```
data/{ID}_{data}_trials.csv
```

Zawiera dla każdej próby: ID uczestnika, wiek, płeć, numer próby, rozmiar sekwencji, % poprawności matematycznej, % poprawności pamięciowej, wyświetlone i przypomniane litery.

## Struktura projektu

```
src/
  main.py               # punkt wejścia, przepływ badania
  engine.py             # logika jednej próby (litery, równania)
  UI.py                 # ekrany (instrukcja, recall, przerwa)
  participiant_info.py  # formularz danych uczestnika, zapis CSV
  config.yaml           # parametry badania
  instructions.txt      # treść instrukcji dla uczestnika
data/                   # wyniki (ignorowane przez git)
```
