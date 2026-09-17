"""
Basic Kalender-App (Kivy-Version)
-----------------------------------
Erster Schritt: Eine Oberfläche, die Termine (Events) anzeigt und
automatisch nach Datum sortiert - jetzt inklusive Kosten und
Teilnehmerzahl, und mit Kivy statt tkinter gebaut.

Die Termine sind aktuell als Beispieldaten im Code hinterlegt.
Im nächsten Schritt bauen wir eine Möglichkeit, neue Termine über
die Oberfläche selbst hinzuzufügen.
"""

from datetime import date

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# ---------------------------------------------------------
# 1. Die Daten: Eine Liste von Terminen
# ---------------------------------------------------------
# Jeder Termin ist ein "Dictionary" mit benannten Feldern. Die
# Schlüssel stehen hier einheitlich klein geschrieben - bei
# Dictionaries muss die Schreibweise beim Zugriff immer exakt
# passen, ein einheitliches Schema vermeidet also Tippfehler.

termine = [
    {"datum": date(2026, 9, 15), "titel": "Kuchenverkauf-Pause", "kosten": "35€", "teilnehmer": "8"},
    {"datum": date(2026, 9, 10), "titel": "Unescolauf", "kosten": "15€", "teilnehmer": "4"},
    {"datum": date(2026, 12, 24), "titel": "Vorfi", "kosten": "1500€", "teilnehmer": "12"},
    {"datum": date(2026, 9, 9), "titel": "Marktstand", "kosten": "100€", "teilnehmer": "8"},
]


# ---------------------------------------------------------
# 2. Eine Funktion, die die Termine nach Datum sortiert
# ---------------------------------------------------------
def sortiere_nach_datum(termin_liste):
    """Gibt die Termine sortiert nach Datum zurück (frühester Termin zuerst)."""
    return sorted(termin_liste, key=lambda termin: termin["datum"])


# ---------------------------------------------------------
# 3. Die Oberfläche (GUI) mit Kivy
# ---------------------------------------------------------
# Kivy ist - anders als tkinter - NICHT bei Python dabei und muss
# einmalig installiert werden:
#
#     pip install kivy
#
# In Kivy baut man Oberflächen aus "Widgets", die man in Layouts
# anordnet. Ein GridLayout ordnet Widgets wie eine Tabelle in
# Zeilen und Spalten an - das nutzen wir jetzt für die vier
# Spalten Datum, Titel, Kosten und Teilnehmer.

SPALTEN = ["Datum", "Titel", "Kosten", "Teilnehmer"]  # Großgeschrieben: Konvention für Konstanten


class KalenderLayout(BoxLayout):
    """Der Aufbau des Fensters: Überschrift oben, Tabelle darunter."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)

        ueberschrift = Label(
            text="Meine Termine",
            font_size="22sp",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=40,
        )
        self.add_widget(ueberschrift)

        # ScrollView, damit die Liste auch bei vielen Terminen
        # später noch auf den Bildschirm passt
        scroll = ScrollView(size_hint=(1, 1))

        self.tabelle = GridLayout(cols=4, spacing=4, size_hint_y=None)
        self.tabelle.bind(minimum_height=self.tabelle.setter("height"))

        scroll.add_widget(self.tabelle)
        self.add_widget(scroll)

        self.termine_anzeigen()

    def termine_anzeigen(self):
        self.tabelle.clear_widgets()

        # Kopfzeile der Tabelle
        for spalte in SPALTEN:
            self.tabelle.add_widget(
                Label(text=spalte, bold=True, color=(0, 0, 0, 1), size_hint_y=None, height=32)
            )

        sortierte_termine = sortiere_nach_datum(termine)

        if not sortierte_termine:
            self.tabelle.add_widget(Label(text="Keine Termine vorhanden.", color=(0, 0, 0, 1)))
            return

        for termin in sortierte_termine:
            datum_lesbar = termin["datum"].strftime("%d.%m.%Y")
            werte = (datum_lesbar, termin["titel"], termin["kosten"], termin["teilnehmer"])

            for wert in werte:
                self.tabelle.add_widget(
                    Label(text=str(wert), color=(0, 0, 0, 1), size_hint_y=None, height=32)
                )


class KalenderApp(App):
    title = "Mein Kalender"

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # weißer Hintergrund
        Window.size = (500, 420)
        return KalenderLayout()


# ---------------------------------------------------------
# 4. Programmstart
# ---------------------------------------------------------
if __name__ == "__main__":
    KalenderApp().run()
