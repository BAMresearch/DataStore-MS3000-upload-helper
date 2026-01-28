# MS3000 Parser & OpenBIS Upload

Strukturierte Python-Module zum Einlesen von Exporten des Malvern Mastersizer3000 zur Partikelgrößenanalyse , Erzeugen von Ergebnisplots/Dateien
und Hochladen der Daten in den BAM Data Store (OpenBIS/ELN) via `pybis`.


## Modulübersicht

- **`config.py`**: Host & IDs für `pybis` (**space**, **project**, **collection**) sowie Zuordnung zum **Parent-Gerät**.
- **`parser.py`**: Lädt die MS3000-Textdatei (UTF‑16), extrahiert Metadaten und Messreihen, vereinheitlicht Datumsformate.
- **`attachs.py`**: Erzeugt `*_results.txt`, `*_freq.png`, `*_sum.png`, `*_preview.png`.
- **`object.py`**: Baut das OpenBIS-Objekt und schreibt alle Metadaten/ELN-Seiten.
- **`openbis.py`**: Login bei OpenBIS und Upload von Objekt & Attachments.

## Voraussetzungen

- Python 3.10+
- Pakete: `pybis`, `matplotlib`
- `tkinter` (für den Dateiauswahldialog, meist in Standard-Python enthalten)

Installation (Beispiel):

```bash
pip install pybis matplotlib
```

## Schnellstart (Beispielskript)

Nach dem Konfigurieren von `config.py` (Host, Space, Project, Collection, Parent-Gerät):

```python
import parser
import attachs
import object as obj_mod
import openbis as ob

# 1) Datei wählen & parsen
file_path = parser.choose_file("MS3000-Datei auswählen")
parsed = parser.parse_ms300_file(file_path)

# 2) Outputs erzeugen
results_file, freq_file, sum_file, preview_file = attachs.make_outputs(parsed)

# 3) Login bei OpenBIS (optional mit PAT-Namen)
o = ob.login(pat_name='test-session')

# 4) OpenBIS-Objekt erstellen
my_object = obj_mod.create_openbis_object(o, parsed["metadata"])

# 5) Upload von Originaldatei + Ergebnissen & Preview
o_bis_dataset, o_bis_preview = ob.upload(
    o,
    my_object,
    [file_path, results_file, freq_file, sum_file],
    preview_file,
)

print("Upload abgeschlossen.")
```

## Hinweise

- **Datumsfelder** werden automatisch ins Format `YYYY-MM-DD HH:MM:SS` konvertiert.
- Der **Diagrammtitel** wird aus `Probenname`, `Proben ID` und `Messdatensatz-Nr.` zusammengesetzt.
- Das **Parent-Gerät** wird (wie im Originalskript) gesetzt, falls die Geräte-Seriennummer `MAL1222865` ist.
- Dataset-Typen: `ATTACHMENT` (Dateisammlung) und `ELN_PREVIEW` (Vorschaubild).

## Projektstruktur

```
.
├── config.py
├── parser.py
├── attachs.py
├── object.py
├── openbis.py
└── README.md
```

## Lizenz

Füge hier deine bevorzugte Lizenz hinzu (z. B. MIT).
