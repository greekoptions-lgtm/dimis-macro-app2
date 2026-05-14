import streamlit as st

st.set_page_config(page_title="Dimis Macro App", layout="centered")

st.title("📊 Dimis Macro Position Sizer")

# Καταχώρηση Score - Τώρα είναι στην κεντρική οθόνη
score = st.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=47)

# Είσοδος Χρήστη
capital = st.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
risk = st.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

if st.button("Υπολογισμός Θέσης"):
    mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
    exposure = (score / 100) * mult[risk]
    exposure = max(0.0, min(1.0, exposure))
    
    inv = capital * exposure
    res = capital - inv
    
    st.divider()
    st.subheader(f"Προτεινόμενη Επένδυση: {inv:,.2f}€")
    st.info(f"Απόθεμα σε Stablecoins: {res:,.2f}€")
    st.caption(f"Ποσοστό έκθεσης: {exposure*100:.1f}%")
