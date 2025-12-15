import streamlit as st
import pandas as pd

def render_risk_section():
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        st.header("⚠️ Risk Analysis")

        df = pd.DataFrame(results)
        high_risk_df = df[df['risk_level'] == 'High']
        medium_risk_df = df[df['risk_level'] == 'Medium']

        st.subheader("High Risk Clauses")
        if not high_risk_df.empty:
            st.dataframe(high_risk_df[['clause_id', 'clause', 'summary']], use_container_width=True)
        else:
            st.info("✅ No high-risk clauses found.")

        st.subheader("Medium Risk Clauses")
        if not medium_risk_df.empty:
            st.dataframe(medium_risk_df[['clause_id', 'clause', 'summary']], use_container_width=True)
        else:
            st.info("✅ No medium-risk clauses found.")
    else:
        st.info("Upload and analyze a contract first in the Upload section.")
