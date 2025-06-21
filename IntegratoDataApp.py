import streamlit as st

st.set_page_config(page_title="Performance & Wellness Hub", page_icon="💡", layout="wide")

# Encabezado con logo
st.markdown(
    """
    <div style="display: flex; align-items: center; margin-bottom: 25px;">
        <img src="https://tmssl.akamaized.net//images/wappen/head/45457.png?lm=1534711579"
             width="70" style="margin-right: 15px; opacity: 0.6;">
        <h1 style="margin: 0;">🏥 Performance & Wellness Hub</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Welcome to the **central dashboard** for player monitoring, wellness, and recovery tracking. Choose one of the following sections:")

# Botones grandes estilo tarjetas
st.markdown("""
<style>
.button-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 500px;
}

.big-button {
    display: block;
    background-color: #f0f2f6;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    text-decoration: none;
    color: black;
    font-size: 1.1rem;
    font-weight: bold;
    border: 1px solid #d0d0d0;
    transition: all 0.2s ease;
}

.big-button:hover {
    background-color: #e0e0e0;
    box-shadow: 0 0 6px rgba(0,0,0,0.1);
    cursor: pointer;
}
</style>

<div class="button-container">
    <a class="big-button" href="./Wellness">📊 Wellness Dashboard</a>
    <a class="big-button" href="./Procedures">💆‍♂️ Physiotherapy Procedures</a>
    <a class="big-button" href="./Calendar">📅 Individual Activity Calendar</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Developed by Edu Caro • Performance Science Department")
