import streamlit as st
import pandas as pd
import numpy as np
import datetime

# -------------------------
# Streamlit Layout
# -------------------------
st.set_page_config(page_title="Dimis Macro Position Sizer", layout="wide")
st.title("📊 Dimis Macro Position Sizer")

# Sidebar inputs
with st.sidebar:
    st.header("Ρυθμίσεις Επένδυσης")
    score = st.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=33)
    capital = st.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
    risk = st.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

    st.markdown("---")
    st.markdown("📌 Δοκίμασε το [Tangem Wallet](https://tangem.com/) για ασφαλή crypto wallets")
    st.markdown("🔥 Ξεκίνα με crypto στο [Bybit](https://www.bybit.eu/b/DIMISGROP/)")

# -------------------------
# Compute position
# -------------------------
mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
exposure = (score / 100) * mult[risk]
exposure = max(0.0, min(1.0, exposure))

investment = capital * exposure
stablecoins = capital - investment

# -------------------------
# Format large numbers
# -------------------------
def format_large(x):
    if x >= 1_000_000_000_000:
        return f"{x/1_000_000_000_000:.2f}T"
    elif x >= 1_000_000_000:
        return f"{x/1_000_000_000:.2f}B"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.2f}M"
    else:
        return f"{x:,.2f}"

# -------------------------
# Layout with columns
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Επένδυση σε crypto")
    st.markdown(f"""
    <div style="font-size:22px; font-weight:bold; color:#000;">
        {format_large(investment)} €
    </div>
    <div style="font-size:14px; color:green;">
        ↑ {exposure*100:.1f}%
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Απόθεμα σε Stablecoins")
    st.markdown(f"""
    <div style="font-size:22px; font-weight:bold; color:#000;">
        {format_large(stablecoins)} €
    </div>
    """, unsafe_allow_html=True)

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

# -------------------------
# Optional: Historical positions chart
# -------------------------
dates = [datetime.date.today() - datetime.timedelta(weeks=i) for i in range(10)][::-1]
positions = [(score/100) * mult["Μέτριο"] * capital * np.random.uniform(0.9,1.1) for _ in range(10)]
df_hist = pd.DataFrame({"Date": dates, "Position": positions})
df_hist["Position Display"] = df_hist["Position"].apply(format_large)

st.subheader("Ιστορικά Προτεινόμενης Θέσης")
st.line_chart(df_hist.set_index("Date")["Position"])
