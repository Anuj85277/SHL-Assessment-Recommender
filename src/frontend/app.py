import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Finder", page_icon="🔍")

st.title("🔍 SHL Assessment Recommender")
st.markdown("Enter a job role or required skills below to find the most relevant SHL tests.")

# Input section
query = st.text_input("Job Role / Skills:", placeholder="e.g. Python Developer, Leadership, Sales...")
n_results = st.slider("Number of recommendations:", 1, 10, 5)

if st.button("Get Recommendations"):
    if query:
        with st.spinner("Searching SHL Catalog..."):
            try:
                # --- UPDATED SECTION ---
                # Changed from requests.get to requests.post
                # Using 'json=' instead of 'params=' to match the Pydantic BaseModel
                response = requests.post(
                    "http://127.0.0.1:8000/recommend", 
                    json={"query": query, "n": n_results}
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    
                    st.subheader(f"Top {len(data['recommendations'])} Recommendations:")
                    
                    for i, rec in enumerate(data['recommendations'], 1):
                        with st.container():
                            st.markdown(f"### {i}. {rec['name']}")
                            st.link_button("View Assessment", rec['url'])
                            st.divider()
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                # -----------------------
                        
            except Exception as e:
                st.error(f"Could not connect to the API. Make sure main.py is running! Error: {e}")
    else:
        st.warning("Please enter a query first.")