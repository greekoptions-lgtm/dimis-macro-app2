import streamlit as st
import pandas as pd

# Ρύθμιση Σελίδας
st.set_page_config(page_title="Dimis Macro App", layout="centered")

# Τίτλος στα Ελληνικά
st.title("📊 Dimis Macro Position Sizer")
st.write("Υπολογίστε την ιδανική έκθεση βάσει του Macro Score.")

# Δεδομένα από το δικό σου Excel (Overall Score: 47)
score = st.sidebar.number_input("Τρέχον Macro Score:", value=47)

# Είσοδος Χρήστη
capital = st.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
risk = st.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

if st.button("Υπολογισμός Θέσης"):
    # Λογική υπολογισμού
    mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
    exposure = (score / 100) * mult[risk]
    
    # Περιορισμός έκθεσης μεταξύ 0 και 100%
    exposure = max(0.0, min(1.0, exposure))
    
    inv = capital * exposure
    res = capital - inv
    
    # Εμφάνιση Αποτελεσμάτων
    st.success(f"Προτεινόμενη Επένδυση: {inv:,.2f}€")
    st.info(f"Απόθεμα σε Stablecoins: {res:,.2f}€")
    st.write(f"Ποσοστό έκθεσης στην αγορά: {exposure*100:.1f}%")
