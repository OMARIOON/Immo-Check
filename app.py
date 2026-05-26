import streamlit as st
import pandas as pd

# App-Konfiguration
st.set_page_config(page_title="Immobilien-Rendite-Prüfer", page_icon="🏢", layout="wide")

st.title("🏢 Immobilien-Rendite-Prüfer (Inkl. Möblierung & Steuern)")
st.write("Berechne den exakten Cashflow deiner Kapitalanlage – jetzt auch für möblierte All-Inclusive-Vermietung.")

st.divider()

# --- SIDEBAR: EINGABEFELDER ---
st.sidebar.header("🔍 1. Projektdaten & Link")
immoscout_link = st.sidebar.text_input("ImmoScout24 Link (optional)", placeholder="https://www.immobilienscout24.de/expose/...")

if immoscout_link:
    st.sidebar.caption("🔗 [Link im neuen Tab öffnen](%s)" % immoscout_link)

st.sidebar.header("💰 2. Finanzielle Rahmendaten")
kaufpreis = st.sidebar.number_input("Kaufpreis (€)", min_value=0.0, value=344900.0, step=5000.0)
nebenkosten_pzt = st.sidebar.slider("Kaufnebenkosten (Grunderwerbsteuer, Notar, Makler in %)", 0.0, 15.0, 5.5, step=0.1)
eigenkapital = st.sidebar.number_input("Eingesetztes Eigenkapital (€)", min_value=0.0, value=0.0, step=2000.0)

st.sidebar.header("📉 3. Finanzierung & Steuer")
zinssatz = st.sidebar.number_input("Zinssatz p.a. (%)", min_value=0.0, value=4.7, step=0.1) / 100
tilgung = st.sidebar.number_input("Tilgung p.a. (%)", min_value=0.0, value=1.1, step=0.1) / 100
steuersatz = st.sidebar.slider("Dein persönlicher Steuersatz (%)", 0, 45, 42) / 100

st.sidebar.header("🏢 4. Mieteinnahmen")
kaltmiete_monat = st.sidebar.number_input("Erwartete Brutto-Miete / Pauschalmiete (monatlich in €)", min_value=0.0, value=1650.0, step=50.0)

st.sidebar.header("🏠 5. Laufende Kosten & Gebäude-Abschreibung")
hausgeld_nicht_umlagbar = st.sidebar.number_input("Nicht umlagefähiges Hausgeld + Rücklage (monatlich in €)", min_value=0.0, value=100.0, step=5.0)
afa_pzt = st.sidebar.slider("Gebäude-AfA-Satz (Abschreibung in %)", 0.0, 5.0, 5.0, step=0.5) / 100
gebaeudeanteil = st.sidebar.slider("Gebäudewert-Anteil für AfA (%)", 0, 100, 80) / 100

# NEU: Sektion für Möblierung
st.sidebar.header("🛋️ 6. Möblierung & Einrichtung")
st.sidebar.caption("Kosten für die Erstausstattung der 1-Zimmerwohnung. Wird steuerlich über 5 Jahre abgeschrieben.")
wert_kueche = st.sidebar.number_input("Einbauküche (€)", min_value=0.0, value=4500.0, step=500.0)
wert_moebel = st.sidebar.number_input("Möbel (Bett, Schrank, Sofa, Esstisch etc. in €)", min_value=0.0, value=3500.0, step=500.0)
wert_geraete = st.sidebar.number_input("Geräte & Deko (TV, Lampen, Geschirr etc. in €)", min_value=0.0, value=1000.0, step=100.0)

# NEU: Sektion für laufende Inklusiv-Kosten
st.sidebar.header("🔌 7. Laufende Inklusiv-Kosten")
st.sidebar.caption("Kosten, die du bei einer Pauschalmiete selbst für den Mieter bezahlst.")
kosten_strom_internet = st.sidebar.number_input("Strom & Internet/WLAN (monatlich in €)", min_value=0.0, value=70.0, step=5.0)
kosten_waerme_wasser = st.sidebar.number_input("Umlagefähige Nebenkosten (Heizung, Wasser etc. monatlich in €)", min_value=0.0, value=90.0, step=5.0)


# --- BERECHNUNGSLOGIK ---
kaufnebenkosten = kaufpreis * (nebenkosten_pzt / 100) 
gesamtkosten = kaufpreis + kaufnebenkosten
darlehen = max(0.0, gesamtkosten - eigenkapital)

# Monatliche Kreditrate
zins_monat = (darlehen * zinssatz) / 12
tilgung_monat = (darlehen * tilgung) / 12
rate_monat = zins_monat + tilgung_monat

# Berechnung Möbel-Abschreibung (AfA über 5 Jahre = 20% pro Jahr)
gesamt_moebel_wert = wert_kueche + wert_moebel + wert_geraete
moebel_afa_jahr = gesamt_moebel_wert * 0.20
moebel_afa_monat = moebel_afa_jahr / 12

# Laufende Gesamtkosten (Hausgeld + Strom + Heizung)
laufende_kosten_gesamt_monat = hausgeld_nicht_umlagbar + kosten_strom_internet + kosten_waerme_wasser

# Cashflow VOR Steuern (Einnahme minus Bankrate minus alle realen Kosten vom Konto)
cashflow_vor_steuer = kaltmiete_monat - rate_monat - laufende_kosten_gesamt_monat

# Steuerliche Betrachtung (Jahr)
miete_jahr = kaltmiete_monat * 12
zins_jahr = darlehen * zinssatz
gebaeude_afa_jahr = (kaufpreis * gebaeudeanteil) * afa_pzt
laufende_kosten_jahr = laufende_kosten_gesamt_monat * 12

# Zu versteuerndes Einkommen unter Berücksichtigung der neuen Möbel-AfA und Inklusivkosten
zu_versteuerndes_einkommen = miete_jahr - zins_jahr - gebaeude_afa_jahr - laufende_kosten_jahr - moebel_afa_jahr
steuerlast_jahr = zu_versteuerndes_einkommen * steuersatz
steuer_monat = steuerlast_jahr / 12

# Cashflow NACH Steuern
cashflow_nach_steuer = cashflow_vor_steuer - steuer_monat

# Wirtschaftlicher Gesamtgewinn (Cashflow + Tilgung)
wirtschaftlicher_gewinn_monat = cashflow_nach_steuer + tilgung_monat


# --- AUSGABE / DASHBOARD ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Gesamtinvestition")
    st.write(f"**Immobilien-Kaufpreis:** {kaufpreis:,.2f} €")
    st.write(f"**Kaufnebenkosten ({nebenkosten_pzt}%):** {kaufnebenkosten:,.2f} €")
    st.write(f"**Gesamtkosten Investition:** {gesamtkosten:,.2f} €")
    st.write(f"**Benötigtes Darlehen:** {darlehen:,.2f} €")
    st.write(f"**Zusätzliche Möblierungskosten (Bar/Eigenkapital):** {gesamt_moebel_wert:,.2f} €")

with col2:
    st.subheader("📈 Steuerliche Abschreibungen (Jahr)")
    st.write(f"**Gebäudewert-Basis ({int(gebaeudeanteil*100)}%):** {(kaufpreis * gebaeudeanteil):,.2f} €")
    st.write(f"**Jährliche Gebäude-AfA ({afa_pzt*100}%):** {gebaeude_afa_jahr:,.2f} €")
    st.write(f"**Jährliche Möbel-AfA (20% p.a.):** {moebel_afa_jahr:,.2f} €")
    
    if zu_versteuerndes_einkommen < 0:
        st.success(f"📉 Steuerlicher Verlust: {zu_versteuerndes_einkommen:,.2f} € (Erzeugt Steuerersparnis!)")
    else:
        st.warning(f"📈 Steuerlicher Gewinn: {zu_versteuerndes_einkommen:,.2f} € (Erzeugt Steuerlast)")

st.divider()

# Cashflow KPIs
st.subheader("💰 Cashflow Analyse (Monatlich)")
kpi1, kpi2 = st.columns(2)

with kpi1:
    if cashflow_vor_steuer >= 0:
        st.metric(label="Cashflow VOR Steuern", value=f"{cashflow_vor_steuer:.2f} €", delta="Positiv")
    else:
        st.metric(label="Cashflow VOR Steuern", value=f"{cashflow_vor_steuer:.2f} €", delta="Negativ", delta_color="inverse")

with kpi2:
    if cashflow_nach_steuer >= 0:
        st.metric(label="Cashflow NACH Steuern", value=f"{cashflow_nach_steuer:.2f} €", delta="Investition trägt sich")
    else:
        st.metric(label="Cashflow NACH Steuern", value=f"{cashflow_nach_steuer:.2f} €", delta="Zuschussgeschäft", delta_color="inverse")

# Detaillierte Tabelle
st.subheader("📋 Einzelposten-Aufschlüsselung (Monatlich)")

daten_tabelle = {
    "Posten": [
        "Mieteinnahmen (Brutto/Pauschalmiete)", 
        "🪓 Davon Zinszahlung (Bank)", 
        "🪓 Davon Tilgung (Vermögensaufbau)", 
        "🪓 Davon Hausgeld (nicht umlagefähig)",
        "🪓 Davon Strom & Internet (Inklusivleistung)",
        "🪓 Davon Heizung & Wasser (Inklusivleistung)",
        "= Cashflow VOR Steuern",
        "⚖️ Steuereffekt (Minus = Last / Plus = Ersparnis)",
        "🚀 FINALES ERGEBNIS: Cashflow NACH Steuern"
    ],
    "Betrag": [
        f"+ {kaltmiete_monat:.2f} €",
        f"- {zins_monat:.2f} €",
        f"- {tilgung_monat:.2f} €",
        f"- {hausgeld_nicht_umlagbar:.2f} €",
        f"- {kosten_strom_internet:.2f} €",
        f"- {kosten_waerme_wasser:.2f} €",
        f"{cashflow_vor_steuer:.2f} €",
        f"{-steuer_monat:.2f} €",
        f"{cashflow_nach_steuer:.2f} €"
    ]
}

df = pd.DataFrame(daten_tabelle)
st.table(df)

# Fazit-Box
st.subheader("💡 Fazit")
if cashflow_nach_steuer > 0:
    st.success(f"**Hervorragend!** Diese Immobilie wirft nach Steuern jeden Monat **{cashflow_nach_steuer:.2f} €** ab. Sie ist ein echter Selbstläufer.")
elif cashflow_nach_steuer == 0:
    st.info("**Punktlandung!** Die Immobilie trägt sich nach Steuern exakt von selbst. Du baust Vermögen auf, ohne monatlich draufzuzahlen.")
else:
    st.error(f"**Achtung Zuschussgeschäft!** Du musst monatlich **{abs(cashflow_nach_steuer):.2f} €** aus eigener Tasche dazuzahlen, um die Immobilie zu halten.")

st.divider()

# --- SEKTION VERMÖGENSAUFBAU ---
st.subheader("🧱 🛠️ Visualisierung des Vermögensaufbaus")
st.write("Der Mieter zahlt deinen Kredit ab, während das Finanzamt dir unterjährig hilft:")

col_v1, col_v2 = st.columns(2)

with col_v1:
    st.info(f"**Monatliche Tilgung (Kreditabbau):** {tilgung_monat:,.2f} €\n\n"
            f"**Wirtschaftlicher Gesamtgewinn p.m.:** {wirtschaftlicher_gewinn_monat:,.2f} €\n"
            f"*(Cashflow nach Steuern + Tilgung)*")

with col_v2:
    vermoegen_1_jahr = tilgung_monat * 12
    vermoegen_5_jahre = tilgung_monat * 12 * 5
    vermoegen_10_jahre = tilgung_monat * 12 * 10
    
    daten_vermoegen = {
        "Zeitraum": ["Nach 1 Jahr", "Nach 5 Jahren", "Nach 10 Jahren"],
        "Abbezahlter Kredit (= Dein Vermögen)": [
            f"{vermoegen_1_jahr:,.2f} €",
            f"{vermoegen_5_jahre:,.2f} €",
            f"{vermoegen_10_jahre:,.2f} €"
        ]
    }
    df_vermoegen = pd.DataFrame(daten_vermoegen)
    st.table(df_vermoegen)
