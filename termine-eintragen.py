"""
Installation & Start
---------------------
    pip install streamlit
    streamlit run termine.py

Die App öffnet sich automatisch im Browser (Standard: http://localhost:8501).
Alle erstellten Veranstaltungen werden dauerhaft in "veranstaltungen.json"
im selben Ordner gespeichert.
"""

import json
import os
from datetime import date, time

import streamlit as st

DATEINAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veranstaltungen.json")


def veranstaltungen_laden():
    if os.path.exists(DATEINAME):
        with open(DATEINAME, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def veranstaltungen_speichern(veranstaltungen):
    with open(DATEINAME, "w", encoding="utf-8") as f:
        json.dump(veranstaltungen, f, ensure_ascii=False, indent=2)


st.set_page_config(page_title="Veranstaltung erstellen")

st.title("Neue Veranstaltung erstellen")


with st.form("neue_veranstaltung", clear_on_submit=True):
    name = st.text_input("Name der Veranstaltung", placeholder="z. B. Vorabi")
    datum = st.date_input("Datum", value=date.today())
    uhrzeit = st.time_input("Uhrzeit", value=time(19, 0))
    ort = st.text_input("Ort", placeholder="z. B. Juki")
    leute = st.number_input("Benötigte Leute", min_value=0, step=1, value=0)

    abschicken = st.form_submit_button("Veranstaltung erstellen", use_container_width=True)

if abschicken:
    if not name.strip() or not ort.strip():
        st.error("Bitte mindestens Name und Ort ausfüllen.")
    else:
        veranstaltungen = veranstaltungen_laden()
        veranstaltungen.append({
            "name": name.strip(),
            "datum": datum.strftime("%Y-%m-%d"),
            "uhrzeit": uhrzeit.strftime("%H:%M"),
            "ort": ort.strip(),
            "leute": int(leute),
        })
        veranstaltungen_speichern(veranstaltungen)
        st.success(f"„{name}“ wurde erstellt und gespeichert!")
