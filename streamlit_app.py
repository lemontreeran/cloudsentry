import streamlit as st
from st_pages import add_page_title


st.set_page_config(layout='wide')
sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

pg = st.navigation([
    st.Page("pages/home.py", title="Home", icon="🔥"),
    st.Page("pages/attack_path_analysis.py", title="Attack Path", icon="📑"),
    st.Page("pages/policy_generation.py", title="Policy Gen", icon="🤖"),
    # st.Page("pages/cloud_policy_verification.py", title="Tableau", icon="🖥️"),
])

add_page_title(pg)

pg.run()