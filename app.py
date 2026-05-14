import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# -------------------------
# Google Sheets Setup
# -------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CREDS = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
GSHEET = "dimis_macro_ai_brief_api_base"  # όνομα Google Sheets
SHEET_SNAPSHOT = "WEEKLY_SNAPSHOT"

gc = gspread.authorize(CREDS)
sh = gc.open(GSHEET)
ws_snapshot = sh.worksheet(SHEET_SNAPSHOT)

# Load weekly snapshot
data = ws_snapshot.get_all_records()
df = pd.DataFrame(data)
df["Snapshot Date"] = pd.to_datetime(df["Snapshot Date"], dayfirst=True)
df = df.sort_values("Snapshot Date", ascending=True)

# Get latest week
latest = df.iloc[-1]
latest_score = latest["Overall Score"]

# -------------------------
# Streamlit Layout
# -------------------------
st.set_page_config(page_title="Dimis Macro Position Sizer", layout="wide")
st.title("📊 Dimis Macro Position Sizer")

# Sidebar inputs
with st.sidebar:
    st.header("Ρυθμίσεις")
    score = st.number_input("Εβδομαδιαίο Macro Score (0-100):", min_value=0, max_value=100, value=int(latest_score))
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
Το ποσοστό επένδυσης βασίζεται στο **score της εβδομάδας** από το Dimis Macro Brief.
- Το score κυμαίνεται από 0 έως 100.
- Προσαρμόζεται ανάλογα με το προφίλ ρίσκου.
- Η προτεινόμενη θέση = (Score / 100) * συντελεστής ρίσκου.
- Το υπόλοιπο μένει σε stablecoins για ασφάλεια.
""")

# -------------------------
# Historical positions chart
# -------------------------
st.subheader("Ιστορικά Προτεινόμενης Θέσης")
df["Position"] = (df["Overall Score"]/100) * mult["Μέτριο"] * df["Συνολικό Κεφάλαιο"] if "Συνολικό Κεφάλαιο" in df else 0
st.line_chart(df.set_index("Snapshot Date")["Position"])
