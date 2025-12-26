import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="RCA & ICAP Engine", layout="wide")

st.title("🔧 Quality RCA – ICAP – ROI System")

uploaded_file = st.file_uploader("Upload Complaint Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Complaint Data")
    st.dataframe(df)

    st.subheader("📊 Root Cause Pareto")
    rca_count = df["Root_Cause"].value_counts()
    st.bar_chart(rca_count)

    st.subheader("🤖 RCA Suggestion Engine")
    issue = st.selectbox("Select Issue", df["Issue"].unique())

    suggestions = (
        df[df["Issue"] == issue]
        .groupby("Root_Cause")
        .size()
        .sort_values(ascending=False)
    )

    st.table(suggestions)

    st.subheader("💰 ROI Impact")
    COST_PER_COMPLAINT = 5000
    roi = df.groupby("Root_Cause").size() * COST_PER_COMPLAINT
    st.bar_chart(roi)
