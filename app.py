import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dimis Macro Position Sizer", layout="centered")

st.title("📊 Dimis Macro Position Sizer")

# --- Sidebar για επιλογές χρήστη ---
st.sidebar.header("Ρυθμίσεις")
score = st.sidebar.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=47)
capital = st.sidebar.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
risk = st.sidebar.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 Δοκίμασε το [Tangem Wallet](https://tangem.com) για ασφαλή crypto wallets")
st.sidebar.markdown("🔥 Ξεκίνα με crypto στο [Bybit](https://www.bybit.com)")

# --- Υπολογισμός έκθεσης ---
def calculate_exposure(score, capital, risk):
    mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
    exposure = (score / 100) * mult[risk]
    exposure = max(0.0, min(1.0, exposure))
    inv = capital * exposure
    res = capital - inv
    return exposure, inv, res

exposure, inv, res = calculate_exposure(score, capital, risk)

if st.button("Υπολογισμός Θέσης"):
    # --- Απεικόνιση αποτελεσμάτων ---
    col1, col2 = st.columns([1,1])
    
    color = "#22ab94" if exposure >= 0.6 else "#f7525f" if exposure <= 0.35 else "#f5a623"
    
    with col1:
        st.metric(
            label="Προτεινόμενη Επένδυση",
            value=f"{inv:,.2f}€",
            delta=f"Ποσοστό: {exposure*100:.1f}%",
            delta_color="inverse"
        )
    with col2:
        st.metric(
            label="Απόθεμα σε Stablecoins",
            value=f"{res:,.2f}€"
        )
    
    # --- Expander για λεπτομέρειες ---
    with st.expander("Πώς υπολογίζεται;"):
        st.write(f"""
        - Score: {score} / 100  
        - Risk multiplier για {risk}: {round(exposure / (score/100),2)}  
        - Επένδυση = Score/100 * Risk multiplier * Συνολικό Κεφάλαιο  
        - Stablecoins = Κεφάλαιο - Επένδυση
        """)

    # --- Ιστορικά δεδομένα (mock για παράδειγμα) ---
    st.subheader("Ιστορικά Προτεινόμενης Θέσης")
    history_data = {
        "Ημερομηνία": pd.date_range(start="2026-03-01", periods=8, freq='W'),
        "Score": [40, 45, 50, 48, 52, 47, 50, score],
        "Επένδυση (€)": [6000, 6750, 7500, 7200, 7800, 7050, 7500, inv]
    }
    df = pd.DataFrame(history_data)
    st.line_chart(df.set_index("Ημερομηνία")["Επένδυση (€)"])
    
    st.caption("Το γράφημα δείχνει πώς θα είχε αλλάξει η προτεινόμενη επένδυση ανά εβδομάδα με τα προηγούμενα scores.")
