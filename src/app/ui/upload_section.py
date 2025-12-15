import streamlit as st
import tempfile, os
from utils.contract_analyzer import analyze_contract_file

def render_upload_section():
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'contract_name' not in st.session_state:
        st.session_state.contract_name = ""

    st.subheader("📁 Upload a Contract")
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['pdf', 'docx'],
        help="Limit 20MB per file • PDF, DOCX"
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.session_state.contract_name = uploaded_file.name
        if st.button("🔍 Submit for Analysis"):
            results = analyze_contract(uploaded_file)
            if results:
                st.session_state.analysis_results = results
                st.session_state.analysis_complete = True
                st.success("✅ Contract analyzed successfully!")
                st.rerun()

def analyze_contract(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        with st.spinner("Analyzing contract... This may take a few minutes."):
            analysis_results = analyze_contract_file(tmp_file_path)
        os.unlink(tmp_file_path)
        if analysis_results:
            return analysis_results
        else:
            st.error("Failed to analyze contract")
            return None
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None
