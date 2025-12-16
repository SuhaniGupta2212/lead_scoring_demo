import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lead Scoring Dashboard", layout="wide")

st.title("🔬 3D In-Vitro Lead Generation Dashboard")

# Load data
df = pd.read_csv("leads.csv")

# Scoring logic
def calculate_score(row):
    score = 0

    # Role Fit
    if any(x in row["Title"] for x in ["Toxicology", "Safety", "Hepatic", "Preclinical"]):
        score += 30

    # Company Intent
    if row["Funding_Stage"] in ["Series A", "Series B"]:
        score += 20

    # Technographic
    if row["Uses_InVitro_Tech"] == "Yes":
        score += 15

    # Scientific Intent
    if row["Published_Liver_Paper"] == "Yes":
        score += 40

    # Location Hub
    if row["Company_HQ"] in ["Boston", "Cambridge", "Bay Area", "Basel"]:
        score += 10

    return min(score, 100)

df["Propensity_to_Buy"] = df.apply(calculate_score, axis=1)

# Search
search = st.text_input("🔍 Search by name, title, company or location")

if search:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

# Sort
df = df.sort_values("Propensity_to_Buy", ascending=False)
df.insert(0, "Rank", range(1, len(df) + 1))

st.dataframe(df, use_container_width=True)

# Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv, "qualified_leads.csv", "text/csv")
