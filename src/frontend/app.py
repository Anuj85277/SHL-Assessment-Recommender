import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Finder", page_icon="🔍")

st.title("🔍 SHL Assessment Recommender")
st.markdown("Enter a job role or required skills to find the most relevant SHL tests.")

# Configuration -  Using your LIVE Render URL
# In src/frontend/app.py
API_URL = "https://shl-assessment-recommender-4x8l.onrender.com/recommend"

query = st.text_input("Job Role / Skills:", placeholder="e.g. Java Developer, Leadership...")
n_results = st.slider("Number of recommendations:", 1, 10, 5)

if st.button("Get Recommendations"):
    if query:
        with st.spinner("Searching SHL Catalog..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={"query": query, "n": n_results}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    recs = data.get('recommendations', [])
                    
                    if not recs:
                        st.warning("No specific matches found. Try broadening your keywords.")
                    else:
                        st.subheader(f"Top {len(recs)} Recommendations:")
                        for i, rec in enumerate(recs, 1):
                            with st.container():
                                st.markdown(f"### {i}. {rec['name']}")
                                st.link_button("View Assessment", rec['url'])
                                st.divider()
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: Ensure the Backend API is live. {e}")
    else:
        st.warning("Please enter a query first.")