import streamlit as st
import pandas as pd

# -----------------------------
# App Title
# -----------------------------
st.set_page_config(page_title="Quality RCA System", layout="wide")
st.title("🔧 Quality RCA – ICAP – ROI System")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Complaint Data (Excel or CSV)",
    type=["csv", "xlsx", "xls"]
)

# -----------------------------
# Main Logic
# -----------------------------
if uploaded_file is not None:

    # Read file safely
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ File read error: {e}")
        st.stop()

    # Show raw data
    st.subheader("📋 Complaint Data")
    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # Pareto Chart (Management View)
    # -----------------------------
    st.subheader("📊 Pareto Analysis (Top Root Causes)")
    
    if "Root_Cause" in df.columns:
        pareto_df = (
            df["Root_Cause"]
            .value_counts()
            .reset_index()
        )
        pareto_df.columns = ["Root_Cause", "Count"]
        
        pareto_df["Cumulative_%"] = (
            pareto_df["Count"].cumsum() / pareto_df["Count"].sum() * 100
        )
        
        st.dataframe(pareto_df, use_container_width=True)
        st.line_chart(pareto_df.set_index("Root_Cause")[["Cumulative_%"]])
        
    else:
        st.error("❌ Root_Cause column missing")
    
    
    # -----------------------------
    # Repeat RCA – Management Alert
    # -----------------------------
    st.subheader("🚨 Repeat RCA – Management Attention Required")
    
    repeat_rca = df["Root_Cause"].value_counts()
    repeat_rca = repeat_rca[repeat_rca > 1]
    
    if not repeat_rca.empty:
        st.error("⚠️ Repeat Root Causes Detected (High Risk)")
        st.table(repeat_rca)
    else:
        st.success("✅ No repeat root causes detected")

     
    # -----------------------------
    # ICAP Effectiveness
    # -----------------------------
    st.subheader("📈 ICAP Effectiveness")

    if "ICAP_Status" in df.columns:
        icap_summary = df.groupby("ICAP_Status").size()
        st.bar_chart(icap_summary)
    else:
        st.error("❌ Column 'ICAP_Status' not found in file")
    
    # -----------------------------
    # RCA Summary
    # -----------------------------
    st.subheader("🧠 Top Root Causes")

    if "Root_Cause" in df.columns:
        rca_summary = df["Root_Cause"].value_counts()
        st.table(rca_summary)
    else:
        st.error("❌ Column 'Root_Cause' not found in file")

    # -----------------------------
    # Simple RCA Suggestion Engine
    # -----------------------------
    st.subheader("💡 RCA Suggestion Engine")

    if "Issue" in df.columns and "Root_Cause" in df.columns:
        issue_selected = st.selectbox(
            "Select Issue",
            df["Issue"].unique()
        )

        suggestion = (
            df[df["Issue"] == issue_selected]["Root_Cause"]
            .value_counts()
            .idxmax()
        )

        st.success(
            f"✅ Most common RCA for **{issue_selected}** is: **{suggestion}**"
        )
    else:
        st.error("❌ Required columns: Issue, Root_Cause")

else:
    st.info("⬆️ Please upload an Excel or CSV file to start")
