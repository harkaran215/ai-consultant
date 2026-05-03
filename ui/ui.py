import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/upload-contract/"

st.set_page_config(page_title="AI Legal Ops", layout="centered")

st.title("📄 AI Contract Analyzer")
st.write("Upload a contract and get AI-powered risk analysis")

# Inputs
vendor = st.text_input("Vendor Name")
value = st.number_input("Contract Value", min_value=0.0, step=100.0)

uploaded_file = st.file_uploader("Upload Contract", type=["txt", "pdf"])

if st.button("Analyze Contract"):

    if not vendor or not uploaded_file:
        st.warning("Please fill all fields")
    else:
        with st.spinner("Analyzing contract..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }

            data = {
                "vendor": vendor,
                "value": value
            }

            try:
                response = requests.post(API_URL, files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Analysis Complete")

                    analysis = result["analysis"]

                    # Display results
                    st.subheader("📊 Results")

                    st.write(f"**Risk Level:** {analysis.get('risk_level', 'N/A')}")

                    st.write("**Summary:**")
                    st.write(analysis.get("summary", ""))

                    if "key_issues" in analysis:
                        st.write("**Key Issues:**")
                        for issue in analysis["key_issues"]:
                            st.write(f"- {issue}")

                else:
                    st.error(response.json())

            except Exception as e:
                st.error(f"Error: {e}")