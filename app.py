import streamlit as st

# -------------------------
# Streamlit Layout
# -------------------------
st.set_page_config(page_title="Dimis Macro Position Sizer", layout="wide")
st.title("📊 Dimis Macro Position Sizer")

# Sidebar inputs
with st.sidebar:
    st.header("Ρυθμίσεις")
    score = st.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=50)
    capital = st.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
    risk = st.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

    st.markdown("---")
    st.markdown("📌 Δοκίμασε το [Tangem Wallet](https://tangem.com/) για ασφαλή crypto wallets")
    st.markdown("🔥 Ξεκίνα με crypto στο [Bybit](https://www.bybit.com/)")

# -------------------------
# Compute position
# -------------------------
mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
exposure = (score / 100) * mult[risk]
exposure = max(0.0, min(1.0, exposure))

investment = capital * exposure
stablecoins = capital - investment

# -------------------------
# Layout with columns
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Προτεινόμενη Επένδυση σε crypto")
    st.metric(label="Ποσό (€)", value=f"{investment:,.2f}", delta=f"{exposure*100:.1f}%")

with col2:
    st.subheader("Απόθεμα σε Stablecoins")
    st.metric(label="Ποσό (€)", value=f"{stablecoins:,.2f}")

# -------------------------
# How it's calculated
# -------------------------
with st.expander("Πώς υπολογίζεται;"):
    st.write("""
Το ποσοστό επένδυσης βασίζεται στο **score της εβδομάδας** που εισάγει ο χρήστης.
- Το score κυμαίνεται από 0 έως 100.
- Προσαρμόζεται ανάλογα με το προφίλ ρίσκου.
- Η προτεινόμενη θέση = (Score / 100) * συντελεστής ρίσκου.
- Το υπόλοιπο μένει σε stablecoins για ασφάλεια.
""")
