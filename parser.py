"""
parser.py – Laden und Parsen der MS3000-Textdatei.

Funktionen:
- choose_file(): Öffnet einen Datei-Dialog (tkinter) zur Auswahl der .txt-Datei.
- parse_ms300_file(file_path): Liest die Datei (UTF-16), extrahiert Metadaten und Messreihen,
  normalisiert Datumsformate und erstellt einen Diagrammtitel.
"""
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def choose_file(title: str = "Choose a file") -> str:
    """Öffnet einen Datei-Dialog und gibt den gewählten Dateipfad zurück."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=title)


def parse_ms300_file(file_path: str) -> dict:
    """Parst die MS3000-Datei und gibt ein Dict mit Arrays & Metadaten zurück."""
    with open(file_path, "r", encoding="utf-16") as f:
        lines = f.readlines()

    # Entferne Zeilenumbrüche und splitte nach TAB
    row1 = lines[0].strip().split("\t")
    row2 = lines[1].strip().split("\t")

    # Schreibe die Rohdaten in Listen
    particle_size = [float(x.replace(",", ".")) for x in row1[54:155]]
    frequency = [float(x.replace(",", ".")) for x in row2[54:155]]
    particle_size_undersize = [float(x.replace(",", ".")) for x in row1[155:256]]
    undersize = [float(x.replace(",", ".")) for x in row2[155:256]]

    # Metadaten-Dict
    metadata = {row1[i]: row2[i] for i in range(54)}

    # Datumsformat anpassen (dd.mm.yyyy HH:MM:SS -> yyyy-mm-dd HH:MM:SS)
    def convert_date(val: str) -> str:
        return datetime.strptime(val, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    if 'Analyse Datum Zeit' in metadata:
        metadata['Analyse Datum Zeit'] = convert_date(metadata['Analyse Datum Zeit'])
    if 'Messung Datum Uhrzeit' in metadata:
        metadata['Messung Datum Uhrzeit'] = convert_date(metadata['Messung Datum Uhrzeit'])

    # Diagrammtitel
    probenname_raw = metadata.get('Probenname', '')
    probenname = probenname_raw.split("'")[1] if "'" in probenname_raw else probenname_raw
    dia_title = f"{probenname} {metadata.get('Proben ID')}-{metadata.get('Messdatensatz-Nr.')}"

    return {
        "file_path": file_path,
        "particle_size": particle_size,
        "frequency": frequency,
        "particle_size_undersize": particle_size_undersize,
        "undersize": undersize,
        "metadata": metadata,
        "dia_title": dia_title,
    }
