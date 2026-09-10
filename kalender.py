"""
Basic Kalender-App
-------------------
Erster Schritt: Eine Oberfläche, die Termine (Events) anzeigt und
automatisch nach Datum sortiert.

Die Termine sind aktuell als Beispieldaten im Code hinterlegt.
Im nächsten Schritt bauen wir eine Möglichkeit, neue Termine über
die Oberfläche selbst hinzuzufügen.
"""

import tkinter as tk
from datetime import date

# ---------------------------------------------------------
# 1. Die Daten: Eine Liste von Terminen
# ---------------------------------------------------------
# Jeder Termin ist ein "Dictionary" - eine kleine Datenstruktur mit
# benannten Feldern (hier: "datum" und "titel"). Das sind erstmal nur
# Beispieldaten, damit wir überhaupt etwas anzuzeigen haben. Später
# könnt ihr eigene Termine über die Oberfläche eintragen.

termine = [
    {"datum": date(2026, 9, 15), "titel": "Zahnarzttermin"},
    {"datum": date(2026, 9, 10), "titel": "Geburtstag von Anna"},
    {"datum": date(2026, 12, 24), "titel": "Weihnachten"},
    {"datum": date(2026, 9, 9), "titel": "Mathe-Test"},
]


# ---------------------------------------------------------
# 2. Eine Funktion, die die Termine nach Datum sortiert
# ---------------------------------------------------------
def sortiere_nach_datum(termin_liste):
    """Gibt die Termine sortiert nach Datum zurück (frühester Termin zuerst)."""
    return sorted(termin_liste, key=lambda termin: termin["datum"])


# ---------------------------------------------------------
# 3. Die Oberfläche (GUI) mit tkinter
# ---------------------------------------------------------
# tkinter ist in Python bereits eingebaut - keine extra Installation
# nötig. Eine Klasse bündelt hier alles, was zum Kalender-Fenster
# gehört, damit wir es später leicht erweitern können.

class KalenderApp:
    def __init__(self, fenster):
        self.fenster = fenster
        self.fenster.title("Mein Kalender")
        self.fenster.geometry("380x420")
        self.fenster.configure(bg="white")

        ueberschrift = tk.Label(
            fenster, text="Meine Termine",
            font=("Arial", 16, "bold"), bg="white"
        )
        ueberschrift.pack(pady=15)

        # Bereich, in dem die Terminliste angezeigt wird
        self.liste_bereich = tk.Frame(fenster, bg="white")
        self.liste_bereich.pack(fill="both", expand=True, padx=15)

        self.termine_anzeigen()

    def termine_anzeigen(self):
        # Zuerst alle bisher angezeigten Zeilen entfernen.
        # Das brauchen wir später, wenn ein neuer Termin hinzukommt
        # und die Liste sich aktualisieren soll.
        for eintrag in self.liste_bereich.winfo_children():
            eintrag.destroy()

        sortierte_termine = sortiere_nach_datum(termine)

        if not sortierte_termine:
            tk.Label(self.liste_bereich, text="Keine Termine vorhanden.", bg="white").pack()
            return

        for termin in sortierte_termine:
            datum_lesbar = termin["datum"].strftime("%d.%m.%Y")

            zeile = tk.Frame(self.liste_bereich, bg="#f0f0f0")
            zeile.pack(fill="x", pady=4)

            tk.Label(
                zeile, text=datum_lesbar, font=("Arial", 10, "bold"),
                bg="#f0f0f0", width=10, anchor="w"
            ).pack(side="left", padx=8, pady=6)

            tk.Label(
                zeile, text=termin["titel"], font=("Arial", 10),
                bg="#f0f0f0", anchor="w"
            ).pack(side="left", padx=8, pady=6)


# ---------------------------------------------------------
# 4. Programmstart
# ---------------------------------------------------------
if __name__ == "__main__":
    fenster = tk.Tk()
    app = KalenderApp(fenster)
    fenster.mainloop()
