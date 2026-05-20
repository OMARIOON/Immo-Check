import streamlit as st
import pandas as pd

# App-Konfiguration
st.set_page_config(page_title="Immobilien-Rendite-Prüfer", page_icon="🏢", layout="wide")

st.title("🏢 Immobilien-Rendite-Prüfer (Vor & Nach Steuern)")
st.write("Berechne schnell und unkompliziert den tatsächlichen Cashflow deiner potenziellen Kapitalanlage.")

st.divider()

# --- SIDEBAR: EINGABEFELDER ---
st.sidebar.header("🔍 1. Projektdaten & Link")
immoscout_link = st.sidebar.text_input("ImmoScout24 Link (optional)", placeholder="https://www.immobilienscout24.de/expose/...")

if immoscout_link:
    st.sidebar.caption("🔗 [Link im neuen Tab öffnen](%s)" % immoscout_link)

st.sidebar.header("💰 2. Finanzielle Rahmendaten")
kaufpreis = st.sidebar.number_input("Kaufpreis (€)", min_value=0.0, value=312000.0, step=5000.0)
nebenkosten_pzt = st.sidebar.slider("Kaufnebenkosten (Grunderwerbsteuer, Notar, Makler in %)", 0.0, 15.0, 5.0, step=0.5)
eigenkapital = st.sidebar.number_input("Eingesetztes Eigenkapital (€)", min_value=0.0, value=40000.0, step=2000.0)

st.sidebar.header("📉 3. Finanzierung & Steuer")
zinssatz = st.sidebar.number_input("Zinssatz p.a. (%)", min_value=0.0, value=3.8, step=0.1) / 100
tilgung = st.sidebar.number_input("Tilgung p.a. (%)", min_value=0.0, value=1.5, step=0.1) / 100
steuersatz = st.sidebar.slider("Dein persönlicher Steuersatz (%)", 0, 45, 42) / 100

st.sidebar.header("🏢 4. Immobilenspezifische Werte")
kaltmiete_monat = st.sidebar.number_input("Erwartete Kaltmiete (monatlich in €)", min_value=0.0, value=900.0, step=50.0)
afa_pzt = st.sidebar.slider("AfA-Satz (Abschreibung in %)", 0.0, 5.0, 2.0, step=0.5) / 100
gebaeudeanteil = st.sidebar.slider("Gebäudewert-Anteil für AfA (%)", 0, 100, 80) / 100
hausgeld_nicht_umlagbar = st.sidebar.number_input("Nicht umlagefähiges Hausgeld + Rücklage (monatlich in €)", min_value=0.0, value=50.0, step=5.0)

# --- BERECHNUNGSLOGIK ---
kaufnebenkosten = kaufpreis * (nebenkosten_pzt / 100) 
gesamtkosten = kaufpreis + kaufnebenkosten
darlehen = max(0.0, gesamtkosten - eigenkapital)

# Monatliche Kreditrate
zins_monat = (darlehen * zinssatz) / 12
tilgung_monat = (darlehen * tilgung) / 12
rate_monat = zins_monat + tilgung_monat

# Cashflow VOR Steuern
einnahmen_monat = kaltmiete_monat
ausgaben_monat = rate_monat + hausgeld_nicht_umlagbar
cashflow_vor_steuer = einnahmen_monat - ausgaben_monat

# Steuerliche Betrachtung (Jahr)
miete_jahr = kaltmiete_monat * 12
zins_jahr = darlehen * zinssatz
afa_jahr = (kaufpreis * gebaeudeanteil) * afa_pzt
hausgeld_jahr = hausgeld_nicht_umlagbar * 12

zu_versteuerndes_einkommen = miete_jahr - zins_jahr - afa_jahr - hausgeld_jahr
steuerlast_jahr = zu
