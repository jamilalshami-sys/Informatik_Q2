from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import json
import os

# Dateiname für die Speicherung
EVENTS_FILE = "events.json"

class EventForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Titel
        self.add_widget(Label(text="Event eintragen", font_size=24, bold=True))

        # Name des Events
        self.name_input = TextInput(hint_text="Name des Events (z. B. Team-Meeting)", size_hint=(1, None), height=40)
        self.add_widget(self.name_input)

        # Beschreibung
        self.description_input = TextInput(hint_text="Beschreibung (optional)", size_hint=(1, None), height=60)
        self.add_widget(self.description_input)

        # Datum (optional)
        self.date_input = TextInput(hint_text="Datum (TT.MM.JJJJ, optional)", size_hint=(1, None), height=40)
        self.add_widget(self.date_input)

        # Ort
        self.location_input = TextInput(hint_text="Ort (z. B. Büro, Zoom-Link)", size_hint=(1, None), height=40)
        self.add_widget(self.location_input)

        # Wichtigkeit (optional)
        self.priority_spinner = TextInput(hint_text="Wichtigkeit (z. B. Hoch, Mittel, Niedrig)", size_hint=(1, None), height=40)
        self.add_widget(self.priority_spinner)

        # Button zum Speichern
        self.submit_button = Button(text="Event speichern", size_hint=(1, None), height=50)
        self.submit_button.bind(on_press=self.submit_event)
        self.add_widget(self.submit_button)

        # Button zum Anzeigen aller gespeicherten Events
        self.show_events_button = Button(text="Alle Events anzeigen", size_hint=(1, None), height=50)
        self.show_events_button.bind(on_press=self.show_all_events)
        self.add_widget(self.show_events_button)

    def submit_event(self, instance):
        # Daten sammeln
        event_data = {
            "name": self.name_input.text,
            "description": self.description_input.text,
            "date": self.date_input.text,
            "location": self.location_input.text,
            "priority": self.priority_spinner.text,
        }

        # Überprüfen, ob der Name ausgefüllt ist
        if not event_data["name"]:
            self.show_popup("Fehler", "Bitte gib mindestens einen Namen für das Event ein!")
            return

        # Daten in die JSON-Datei speichern
        self.save_event(event_data)

        # Bestätigung anzeigen
        message = f"Event '{event_data['name']}' wurde gespeichert!"
        self.show_popup("Erfolg", message)

        # Felder zurücksetzen
        self.name_input.text = ""
        self.description_input.text = ""
        self.date_input.text = ""
        self.location_input.text = ""
        self.priority_spinner.text = ""

    def save_event(self, event_data):
        # Lade bestehende Events oder erstelle eine leere Liste
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, "r") as f:
                events = json.load(f)
        else:
            events = []

        # Füge das neue Event hinzu
        events.append(event_data)

        # Speichere die Liste zurück in die Datei
        with open(EVENTS_FILE, "w") as f:
            json.dump(events, f, indent=4)

    def show_all_events(self, instance):
        # Lade alle Events aus der JSON-Datei
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, "r") as f:
                events = json.load(f)
            message = "\n\n".join([f"**{i+1}. Event**\n" + "\n".join([f"{key}: {value}" for key, value in event.items()]) for i, event in enumerate(events)])
        else:
            message = "Keine Events gespeichert."

        self.show_popup("Gespeicherte Events", message)

    def show_popup(self, title, message):
        popup = Popup(title=title, size_hint=(0.8, 0.7))
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Schließen", size_hint=(1, None), height=40)
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        popup.content = content
        popup.open()

class EventFormApp(App):
    def build(self):
        return EventForm()

if __name__ == "__main__":
    EventFormApp().run()
