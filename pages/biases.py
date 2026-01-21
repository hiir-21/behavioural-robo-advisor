import streamlit as st

def show_biases():
    st.header("Behavioral Biases Covered")

    st.markdown("""
    **Loss Aversion** – Preference to avoid losses more strongly than acquiring gains  
    **Anchoring** – Reliance on initial information such as purchase price  
    **Confirmation Bias** – Seeking information that confirms existing beliefs  
    **Herding** – Following actions of the majority  
    **Overconfidence** – Overestimating predictive ability  
    **Disposition Effect** – Selling winners too early and holding losers too long  
    **Status Quo Bias** – Preference for existing choices  
    **Emotional / Overtrading Bias** – Excessive reaction to market movements
    """)

