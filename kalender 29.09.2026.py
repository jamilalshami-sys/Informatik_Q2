

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
#
# Beträge und Teilnehmer sind ZAHLEN (nicht Text), damit wir damit
# rechnen können. None bedeutet "noch unbekannt". Das "€" wird erst
# bei der Anzeige angehängt.

termine = [
    {"datum": date(2026, 9, 15), "titel": "Kuchenverkauf-Pause", "kosten": 35, "teilnehmer": 8, "gewinn": 250},
    {"datum": date(2026, 9, 10), "titel": "Unescolauf", "kosten": 15, "teilnehmer": 4, "gewinn": 212},
    {"datum": date(2026, 12, 24), "titel": "Vorfi", "kosten": 1500, "teilnehmer": 12, "gewinn": None},
    {"datum": date(2026, 9, 9), "titel": "Marktstand", "kosten": 100, "teilnehmer": 8, "gewinn": 360},
    {"datum": date(2026, 10, 9), "titel": "Tiktok Videodreh", "kosten": 0, "teilnehmer": 3, "gewinn": None},
    ]


# ---------------------------------------------------------
# 2. Eine Funktion, die die Termine nach Datum sortiert
# ---------------------------------------------------------
def sortiere_nach_datum(termin_liste):
    """Gibt die Termine sortiert nach Datum zurück (frühester Termin zuerst)."""
    return sorted(termin_liste, key=lambda termin: termin["datum"])


def als_euro(betrag):
    """Macht aus einer Zahl einen Text mit Euro-Zeichen, z. B. 35 -> "35€".
    None (unbekannt) wird zu "?€"."""
    if betrag is None:
        return "?€"
    return f"{betrag}€"


def reingewinn(termin):
    """Gewinn minus Kosten. Ist der Gewinn noch unbekannt, ist es auch
    der Reingewinn (None)."""
    if termin["gewinn"] is None:
        return None
    return termin["gewinn"] - termin["kosten"]


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

SPALTEN = ["Datum", "Titel", "Kosten", "Teilnehmer", "Gewinn", "Reingewinn"]  # Großgeschrieben: Konvention für Konstanten


def zelle(text, bold=False):
    """Erzeugt ein Label für eine Tabellenzelle.

    text_size wird an die Größe der Zelle gebunden: So weiß das Label,
    wie viel Platz es hat. Mit shorten=True wird zu langer Text dann
    mit "..." abgekürzt, statt in die Nachbarspalte zu ragen."""
    label = Label(
        text=text,
        bold=bold,
        color=(0, 0, 0, 1),
        size_hint_y=None,
        height=32,
        shorten=True,
        shorten_from="right",
        halign="center",
        valign="middle",
    )
    label.bind(size=lambda widget, groesse: setattr(widget, "text_size", groesse))
    return label


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

        self.tabelle = GridLayout(cols=len (SPALTEN), spacing=5, size_hint_y=None)
        self.tabelle.bind(minimum_height=self.tabelle.setter("height"))

        scroll.add_widget(self.tabelle)
        self.add_widget(scroll)

        self.termine_anzeigen()

    def termine_anzeigen(self):
        self.tabelle.clear_widgets()

        # Kopfzeile der Tabelle
        for spalte in SPALTEN:
            self.tabelle.add_widget(zelle(spalte, bold=True))

        sortierte_termine = sortiere_nach_datum(termine)

        if not sortierte_termine:
            self.tabelle.add_widget(zelle("Keine Termine vorhanden."))
            return

        for termin in sortierte_termine:
            datum_lesbar = termin["datum"].strftime("%d.%m.%Y")
            werte = (
                datum_lesbar,
                termin["titel"],
                als_euro(termin["kosten"]),
                str(termin["teilnehmer"]),
                als_euro(termin["gewinn"]),
                als_euro(reingewinn(termin)),
            )

            for wert in werte:
                self.tabelle.add_widget(zelle(wert))

        # Summenzeile: Jetzt, wo die Beträge Zahlen sind, können wir rechnen.
        # Unbekannte Gewinne (None) werden beim Addieren übersprungen.
        summe_kosten = sum(t["kosten"] for t in termine)
        summe_gewinn = sum(t["gewinn"] for t in termine if t["gewinn"] is not None)
        summe_rein = sum(reingewinn(t) for t in termine if reingewinn(t) is not None)

        summen = ("", "Gesamt", als_euro(summe_kosten), "", als_euro(summe_gewinn), als_euro(summe_rein))
        for wert in summen:
            self.tabelle.add_widget(zelle(wert, bold=True))


class KalenderApp(App):
    title = "Mein Kalender"

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # weißer Hintergrund
        Window.size = (720, 420)
        return KalenderLayout()


# ---------------------------------------------------------
# 4. Programmstart
# ---------------------------------------------------------
if __name__ == "__main__":
    KalenderApp().run()
