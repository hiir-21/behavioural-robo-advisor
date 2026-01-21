import streamlit as st

def show_navbar():
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    tabs = ["Home", "Methodology", "Biases", "About"]

    for col, tab in zip(cols, tabs):
        with col:
            if st.button(tab, key=f"nav_{tab}"):
                st.session_state.page = tab
                st.rerun()
