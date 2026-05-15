import streamlit as st
import pandas as pd

# -------------------------
# Streamlit Layout
# -------------------------
st.set_page_config(page_title="Dimis Macro Position Sizer", layout="wide")
st.title("📊 Dimis Macro Position Sizer")

# -------------------------
# Sidebar inputs
# -------------------------
with st.sidebar:
    st.markdown("<h3 style='color:#1E90FF'>Ρυθμίσεις Επένδυσης</h3>", unsafe_allow_html=True)
    score = st.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=0)
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
    st.markdown(f"<div style='padding:15px; background-color:#F0F8FF; border-radius:10px'>"
                f"<h4>Προτεινόμενη Επένδυση σε crypto</h4>"
                f"<h2>€{investment:,.2f}</h2></div>", unsafe_allow_html=True)
    st.progress(int(exposure*100))

with col2:
    st.markdown(f"<div style='padding:15px; background-color:#FFF0F5; border-radius:10px'>"
                f"<h4>Απόθεμα σε Stablecoins</h4>"
                f"<h2>€{stablecoins:,.2f}</h2></div>", unsafe_allow_html=True)

# -------------------------
# How it's calculated
# -------------------------
with st.expander("Πώς υπολογίζεται;"):
    st.write("""
Το ποσοστό επένδυσης βασίζεται στο **score της εβδομάδας** που εισάγει ο χρήστης.
- Το score κυμαίνεται από 0 έως 100.
- Προσαρμόζεται ανάλογα με το προφίλ ρίσκου.
- Προτεινόμενη θέση = (Score / 100) * συντελεστής ρίσκου.
- Το υπόλοιπο μένει σε stablecoins για ασφάλεια.
""")

# -------------------------
# Historical positions chart (demo data)
# -------------------------
st.subheader("Ιστορικά Προτεινόμενης Θέσης")

# Δημιουργία demo δεδομένων για chart
dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
scores_demo = [20, 35, 50, 45, 60, 55, 70, 65, 80, score]
df_demo = pd.DataFrame({"Snapshot Date": dates, "Overall Score": scores_demo})
df_demo["Position"] = (df_demo["Overall Score"]/100) * mult["Μέτριο"] * capital

st.line_chart(df_demo.set_index("Snapshot Date")["Position"])
