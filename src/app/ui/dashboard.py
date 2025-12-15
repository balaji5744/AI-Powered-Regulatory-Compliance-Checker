import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard_section():
    if not st.session_state.analysis_results:
        st.info("Upload and analyze a contract first in the Upload section.")
        return

    results = st.session_state.analysis_results
    st.header("📊 Compliance Score")
    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Levels")
        risk_counts = df['risk_level'].value_counts()
        fig_risk = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            color=risk_counts.index,
            color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#44ff44'},
            title="Risk Level Distribution"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        st.subheader("Compliance Status")
        total_clauses = len(results)
        compliant = len([r for r in results if r['risk_level'] == 'Low'])
        non_compliant = total_clauses - compliant
        fig_compliance = go.Figure(data=[go.Pie(
            labels=['Compliant', 'Non-Compliant'],
            values=[compliant, non_compliant],
            hole=0.3,
            marker_colors=['#44ff44', '#ff4444']
        )])
        fig_compliance.update_layout(title="Compliance Ratio")
        st.plotly_chart(fig_compliance, use_container_width=True)

    
    compliant_percentage = (compliant / total_clauses) * 100 if total_clauses > 0 else 0
    high_risk_count = len([r for r in results if r['risk_level'] == 'High'])
    risk_percentages = []
    for r in results:
        try:
            risk_val = r['risk_percent'].replace('%', '').strip()
            risk_percentages.append(float(risk_val))
        except:
            continue
    avg_risk = sum(risk_percentages) / len(risk_percentages) if risk_percentages else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clauses", total_clauses)
    with col2:
        st.metric("Compliance Rate", f"{compliant_percentage:.0f}%")
    with col3:
        st.metric("High Risk Clauses", high_risk_count)
    with col4:
        st.metric("Avg Risk Score", f"{avg_risk:.0f}%")

    if compliant > 0:
        st.success(f"✓ {compliant} clauses compliant")
    else:
        st.warning("No fully compliant clauses found")
