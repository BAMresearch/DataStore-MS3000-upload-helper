#!/usr/bin/env python3
"""
main.py – CLI für MS3000 Parsing & OpenBIS Upload

Nutzung:
    python main.py --file /pfad/zur/datei.txt
    python main.py --dialog
Optionale Parameter:
    --pat-name "test-session"  # erstellt/holt PAT
    --username USER --password PASS  # falls kein Prompt gewünscht

Wenn weder --file noch --dialog gesetzt ist, öffnet das Skript standardmäßig den Dialog.
"""
import sys
import argparse

import parser as ms_parser
import attachs
import object as obj_mod
import openbis as ob


def run_cli(argv=None):
    parser = argparse.ArgumentParser(description="MS3000 → OpenBIS Upload")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--file", type=str, help="Pfad zur MS3000-Textdatei")
    g.add_argument("--dialog", action="store_true", help="Datei über Dialog wählen")

    parser.add_argument("--pat-name", type=str, default="test-session", help="Name für Personal Access Token")
    parser.add_argument("--username", type=str, help="OpenBIS Username (optional)")
    parser.add_argument("--password", type=str, help="OpenBIS Passwort (optional)")
    parser.add_argument("--no-pat", action="store_true", help="Keinen PAT anlegen")

    args = parser.parse_args(argv)

    # 1) Datei bestimmen
    if args.file:
        file_path = args.file
    else:
        # Default: Dialog, auch wenn --dialog nicht explizit gesetzt ist
        title = "MS3000-Datei auswählen" if args.dialog or not args.file else "Choose a file"
        file_path = ms_parser.choose_file(title)
        if not file_path:
            print("Keine Datei ausgewählt.")
            return 1

    print(f"[1/5] Datei: {file_path}")

    # 2) Parsen
    parsed = ms_parser.parse_ms300_file(file_path)
    print("[2/5] Parsing abgeschlossen.")

    # 3) Outputs erzeugen
    results_file, freq_file, sum_file, preview_file = attachs.make_outputs(parsed)
    print("[3/5] Outputs erstellt:")
    print("          ", results_file)
    print("          ", freq_file)
    print("          ", sum_file)
    print("          ", preview_file)

    # 4) Login bei OpenBIS
    pat_name = None if args.no_pat else args.pat_name
    o = ob.login(username=args.username, password=args.password, pat_name=pat_name)
    print("[4/5] Login erfolgreich.")

    # 5) Objekt erstellen & Upload
    my_object = obj_mod.create_openbis_object(o, parsed["metadata"])
    user_dataset, user_preview = ob.upload(
        o,
        my_object,
        [file_path, results_file, freq_file, sum_file],
        preview_file,
    )
    print("[5/5] Upload abgeschlossen.")

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
