import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="PatentMine", layout="wide", page_icon="💡")

# ------------------ MODERN CSS ------------------
st.markdown("""
<style>

body {
    background: #0b0f19;
}

.stApp {
    background: radial-gradient(circle at 20% 20%, #111827, #020617);
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1f2937;
}

/* Title */
.hero {
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#38bdf8,#22c55e);
    color: black;
    font-weight: 600;
    border-radius: 10px;
    height: 45px;
}

/* Inputs */
input, .stSelectbox div {
    border-radius: 10px !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("💡 PatentMine")
page = st.sidebar.radio("Navigate", ["Dashboard", "Search AI", "Analytics"])

# ------------------ HERO ------------------
st.markdown('<div class="hero">Patent Intelligence Engine</div>', unsafe_allow_html=True)
st.markdown("Find **hidden billion-dollar opportunities** in expired patents using AI.")
st.markdown("---")

# ------------------ DASHBOARD ------------------
if page == "Dashboard":

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card">📊 Total Patents<br><h2>12M+</h2></div>', unsafe_allow_html=True)
    col2.markdown('<div class="card">🚀 Opportunities Found<br><h2>84,392</h2></div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">⚡ AI Accuracy<br><h2>94%</h2></div>', unsafe_allow_html=True)

    st.markdown("### 🔥 Trending Domains")

    domains = ["AI", "EV Batteries", "Robotics", "MedTech", "FinTech"]
    cols = st.columns(len(domains))

    for i, d in enumerate(domains):
        cols[i].markdown(f'<div class="card">{d}</div>', unsafe_allow_html=True)

# ------------------ SEARCH PAGE ------------------
elif page == "Search AI":

    st.markdown("### 🧠 AI Opportunity Radar")

    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        keyword = st.text_input("Keyword", placeholder="e.g. solid state battery")

    with col2:
        domain = st.selectbox("Domain", ["", "AI", "EV", "Robotics", "MedTech"])

    with col3:
        country = st.selectbox("Country", ["", "US", "IN", "EP"])

    if st.button("🚀 Scan Opportunities", use_container_width=True):

        with st.spinner("Running deep AI analysis..."):

            try:
                res = requests.get("http://localhost:8000/patents", params={
                    "q": keyword, "domain": domain, "country": country
                })

                data = res.json()

                if not data:
                    st.warning("No results found")
                else:
                    st.success(f"{len(data)} opportunities discovered")

                    # -------- CARD BASED RESULTS ----------
                    for item in data[:8]:

                        st.markdown(f"""
                        <div class="card">
                        <h3>{item['title']}</h3>
                        <p><b>Domain:</b> {item['tech_domain']}</p>
                        <p><b>Score:</b> {item['opportunity_score']}/100</p>
                        <p>{item.get('startup_opportunity','')}</p>
                        </div>
                        """, unsafe_allow_html=True)

            except:
                st.error("Backend not connected")

# ------------------ ANALYTICS ------------------
elif page == "Analytics":

    st.markdown("### 📊 Platform Insights")

    try:
        res = requests.get("http://localhost:8000/stats")
        stats = res.json()

        col1, col2 = st.columns(2)

        col1.metric("Total Patents", stats.get("total_patents", 0))
        col2.metric("Domains", len(stats.get("domains", {})))

        df = pd.DataFrame(list(stats.get("domains", {}).items()), columns=["Domain","Count"])
        st.bar_chart(df.set_index("Domain"))

    except:
        st.warning("No backend data")
