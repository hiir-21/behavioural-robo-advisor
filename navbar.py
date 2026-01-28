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

    /* Target Streamlit buttons inside navbar */
    .navbar button {
        transition: transform 0.2s ease-in-out;
    }

    .navbar button:hover {
        transform: scale(1.08);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="navbar">', unsafe_allow_html=True)

    cols = st.columns(4)
    tabs = ["Home", "Methodology", "Biases", "About"]

    for col, tab in zip(cols, tabs):
        with col:
            if st.button(tab, key=f"nav_{tab}"):
                st.session_state.page = tab
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
