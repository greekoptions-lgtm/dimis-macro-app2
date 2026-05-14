import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Dimis Macro App", layout="wide")
st.title("📊 Dimis Macro Position Sizer")

# --- Sidebar: Settings & Links ---
st.sidebar.header("Ρυθμίσεις")
score = st.sidebar.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=47)
capital = st.sidebar.number_input("Συνολικό Κεφάλαιο (€):", min_value=0, value=10000)
risk = st.sidebar.selectbox("Προφίλ Ρίσκου:", ["Συντηρητικό", "Μέτριο", "Επιθετικό"], index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 Δοκίμασε το [Tangem Wallet](https://tangem.com/) για ασφαλή crypto wallets")
st.sidebar.markdown("🔥 Ξεκίνα με crypto στο [Bybit](https://www.bybit.com/)")

# --- Compute Position ---
mult = {"Συντηρητικό": 0.6, "Μέτριο": 1.0, "Επιθετικό": 1.4}
exposure = (score / 100) * mult[risk]
exposure = max(0.0, min(1.0, exposure))
inv = capital * exposure
res = capital - inv

st.subheader("Υπολογισμός Θέσης")
st.metric("Προτεινόμενη Επένδυση", f"{inv:,.2f}€", delta=f"{exposure*100:.1f}%")
st.info(f"Απόθεμα σε Stablecoins: {res:,.2f}€")

# --- Show Calculation Explanation ---
with st.expander("Πώς υπολογίζεται;"):
    st.write("""
    - Ο weekly Macro Score (0-100) δείχνει τη γενική εικόνα της αγοράς.
    - Το προφίλ ρίσκου επηρεάζει το πόσο μεγάλο μέρος του κεφαλαίου εκτίθεται.
    - Exposure = Score / 100 * Risk Multiplier
    - Investment = Capital * Exposure
    """)

# --- Load Weekly Snapshot for Historical Chart ---
@st.cache_data
def load_snapshot():
    # Αν έχεις το Google Sheets export ως CSV
    df = pd.read_csv("WEEKLY_SNAPSHOT.csv", parse_dates=["Snapshot Date"])
    df["Investment"] = df["Overall Score"] / 100 * df["Total Capital"]
    return df

# --- Example: Fake Data if no CSV ---
import datetime, numpy as np
dates = pd.date_range(end=datetime.date(2026,5,14), periods=10, freq='W')
example_df = pd.DataFrame({
    "Snapshot Date": dates,
    "Investment": [6763, 7200, 7500, 7300, 7800, 7100, 7600, 7300, 7500, 3241]
})

df = example_df  # replace with load_snapshot() if real CSV

# --- Historical Chart ---
st.subheader("Ιστορικά Προτεινόμενης Θέσης")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("Snapshot Date:T", title="Ημερομηνία"),
    y=alt.Y("Investment:Q", title="Προτεινόμενη Επένδυση (€)"),
    tooltip=["Snapshot Date:T", "Investment:Q"]
).properties(width=800, height=400)

st.altair_chart(chart, use_container_width=True)
