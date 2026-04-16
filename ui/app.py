import streamlit as st
import requests
import pandas as pd
import urllib.parse

st.set_page_config(
    page_title="PatentMine",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

# ─── Professional Light Theme CSS ─────────────────────────────────────────────
st.markdown("""
<style>
/* Import clean font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Header strip */
.pm-header {
    background: #1e3a5f;
    color: white;
    padding: 22px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.pm-header h1 {
    margin: 0;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: white;
}
.pm-header p {
    margin: 3px 0 0 0;
    font-size: 0.9rem;
    color: #a8c5e2;
}

/* Search box card */
.search-card {
    background: #ffffff;
    border: 1px solid #e1e8ef;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* Score badge */
.score-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 6px;
}
.badge-green { background: #d1fae5; color: #065f46; }
.badge-blue  { background: #dbeafe; color: #1e40af; }
.badge-gray  { background: #f1f5f9; color: #475569; }
.badge-amber { background: #fef3c7; color: #92400e; }
.badge-red   { background: #fee2e2; color: #991b1b; }

/* Score bar */
.score-bar-wrap { margin: 4px 0 2px 0; }
.score-bar-bg {
    background: #e2e8f0;
    border-radius: 4px;
    height: 7px;
    width: 100%;
}
.score-bar-fill {
    height: 7px;
    border-radius: 4px;
}

/* Patent card expander tweak */
.streamlit-expanderHeader {
    background: #f8fafc !important;
    border-radius: 10px !important;
    border: 1px solid #e1e8ef !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 14px 18px !important;
}
.streamlit-expanderContent {
    border: 1px solid #e1e8ef;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 18px 22px !important;
    background: #ffffff !important;
}

/* Abstract box */
.abstract-box {
    background: #fafbfc;
    border-left: 3px solid #cbd5e1;
    padding: 14px 16px;
    border-radius: 4px;
    font-size: 0.92rem;
    line-height: 1.65;
    color: #374151;
    margin: 10px 0;
}

/* Info box for AI insight */
.insight-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 14px 16px;
    border-radius: 8px;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #1e40af;
    margin-top: 10px;
}

/* Pitch box */
.pitch-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #166534;
    margin: 10px 0;
}

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px 3px 2px 0;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 18px 0;
}

/* Metric cards override */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e1e8ef;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Button clean */
.stButton > button[kind="primary"] {
    background: #1e3a5f;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 20px;
    transition: background 0.2s;
}
.stButton > button[kind="primary"]:hover {
    background: #16304f;
    border: none;
}

/* Tab labels */
button[data-baseweb="tab"] {
    font-weight: 600;
    font-size: 0.95rem;
}

/* Hide hamburger menu */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pm-header">
    <div style="font-size:2rem">🔍</div>
    <div>
        <h1>PatentMine</h1>
        <p>Enterprise Intellectual Property Discovery & Analysis Platform</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  Search Interface  ", "  Dataset Metrics  "])


# ════════════════════════════════════════════════════════════
# TAB 1 — SEARCH
# ════════════════════════════════════════════════════════════
with tab1:

    # ── Search Controls ────────────────────────────────────
    col_search, col_domain, col_country = st.columns([3, 2, 1])
    with col_search:
        keyword = st.text_input(
            "Search Keywords",
            placeholder="e.g. solid-state battery, CRISPR, autonomous navigation",
            label_visibility="visible"
        )
    with col_domain:
        domain = st.selectbox("Technology Domain", [
            "", "Pharmaceuticals", "Semiconductors",
            "Batteries / Energy Storage", "Digital Communications",
            "Wind Energy", "Electric Vehicles", "Robotics",
            "MedTech", "FinTech", "Computing / Software"
        ])
    with col_country:
        country = st.selectbox("Jurisdiction", ["", "US", "IN", "EP", "WO"])

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("Search Patent Database", use_container_width=True, type="primary"):
        with st.spinner("Querying patent database..."):
            try:
                res = requests.get("http://localhost:8000/patents", params={
                    "q": keyword, "domain": domain, "country": country
                })
                res.raise_for_status()
                st.session_state['patents'] = res.json().get("patents", [])
            except Exception as e:
                st.error(f"Unable to connect to backend API: {e}")

    # ── Results ────────────────────────────────────────────
    if 'patents' in st.session_state:
        patents = st.session_state['patents']

        if not patents:
            st.warning("No lapsed patents found matching your search criteria.")
        else:
            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

            # Summary row
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Results Found", len(patents))
            avg_score = round(sum(p.get('score', 0) for p in patents) / len(patents))
            col_b.metric("Avg. Utility Score", f"{avg_score} / 99")
            top_score = max(p.get('score', 0) for p in patents)
            col_c.metric("Top Score", f"{top_score} / 99")
            domains = set(p.get('tech', '') for p in patents if p.get('tech'))
            col_d.metric("Domains Covered", len(domains))

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # Summary table
            with st.expander("📋  Results Overview Table", expanded=True):
                df = pd.DataFrame(patents)
                display_cols = ["id", "title", "assignee", "tech", "lapse", "score"]
                existing_cols = [c for c in display_cols if c in df.columns]
                rename_map = {
                    "id": "Patent ID", "title": "Title", "assignee": "Assignee",
                    "tech": "Domain", "lapse": "Lapse Date", "score": "Utility Score"
                }
                st.dataframe(
                    df[existing_cols].rename(columns=rename_map),
                    use_container_width=True,
                    hide_index=True
                )

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            st.markdown("#### Detailed Patent Analysis (Top 10)")

            # ── Patent Cards ──────────────────────────────
            for item in patents[:10]:
                score      = item.get('score', 0)
                recency    = item.get('recency', 0)
                prestige   = item.get('prestige', 0)
                breadth    = item.get('breadth', 0)
                tech       = item.get('tech', 'Unknown')
                assignee   = item.get('assignee', 'Unknown')
                lapse      = item.get('lapse', 'N/A')
                tags       = item.get('tags', [])
                pitch      = item.get('startup_pitch', '')
                abstract_text = item.get('abstract', 'N/A')

                # Score colour
                if score >= 80:   score_cls = "badge-green"
                elif score >= 65: score_cls = "badge-blue"
                elif score >= 50: score_cls = "badge-amber"
                else:             score_cls = "badge-red"

                tag_html = " ".join(f"<span class='tag-pill'>{t}</span>" for t in tags)

                label = f"**{item['title']}**   ·   Score {score}/99   ·   {tech}"

                with st.expander(label):

                    # Top meta row
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(
                            f"**Assignee:** {assignee}  &nbsp;|&nbsp;  "
                            f"**Jurisdiction:** {item.get('country', 'US / Global')}  &nbsp;|&nbsp;  "
                            f"**Lapse Date:** {lapse}"
                        )
                        st.markdown(tag_html, unsafe_allow_html=True)
                    with c2:
                        st.markdown(
                            f"<span class='score-badge {score_cls}' style='font-size:1.1rem;padding:6px 14px'>"
                            f"Score: {score}</span>",
                            unsafe_allow_html=True
                        )

                    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

                    # Score bars
                    sub_scores = [
                        ("Citations Weighted", score,    "#1e3a8a"),
                        ("Recency",            recency,  "#0369a1"),
                        ("Assignee Prestige",  prestige, "#6d28d9"),
                        ("Claim Breadth",      breadth,  "#065f46"),
                    ]
                    s1, s2, s3, s4 = st.columns(4)
                    for col, (label_s, val, colour) in zip([s1, s2, s3, s4], sub_scores):
                        with col:
                            st.markdown(
                                f"<div style='font-size:0.78rem;color:#6b7280;font-weight:600;margin-bottom:4px'>"
                                f"{label_s}</div>"
                                f"<div class='score-bar-bg'><div class='score-bar-fill' "
                                f"style='width:{val}%;background:{colour}'></div></div>"
                                f"<div style='font-size:0.85rem;font-weight:600;color:{colour};margin-top:3px'>{val}</div>",
                                unsafe_allow_html=True
                            )

                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

                    # Pitch
                    if pitch:
                        st.markdown(
                            f"<div class='pitch-box'>💼 <strong>Commercial Opportunity:</strong> {pitch}</div>",
                            unsafe_allow_html=True
                        )

                    # Abstract
                    st.markdown("<strong>Technical Abstract</strong>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='abstract-box'>{abstract_text}</div>",
                        unsafe_allow_html=True
                    )

                    # AI Summary
                    if len(abstract_text) > 150:
                        if st.button("Generate Executive Summary", key=f"sum_{item['id']}"):
                            with st.spinner("Requesting LLM inference..."):
                                try:
                                    prompt = (
                                        f"Act as a strategic business analyst. Read this patent abstract "
                                        f"and provide exactly 2 sentences explaining the core commercial "
                                        f"value and why an entrepreneur or enterprise should care. "
                                        f"Be precise and strategic, not just descriptive. "
                                        f"Abstract: {abstract_text}"
                                    )
                                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                                    response = requests.get(url, timeout=25)
                                    if response.status_code == 200:
                                        st.markdown(
                                            f"<div class='insight-box'>🧠 <strong>Executive Insight:</strong> {response.text}</div>",
                                            unsafe_allow_html=True
                                        )
                                    else:
                                        st.error(f"LLM inference failed. Status: {response.status_code}")
                                except Exception as e:
                                    st.error(f"Inference error: {e}")

                    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

                    # Action buttons
                    act1, act2 = st.columns([1, 1])
                    with act1:
                        blueprint = (
                            f"PATENT STRATEGY BRIEF\n"
                            f"{'='*50}\n"
                            f"Title:    {item['title']}\n"
                            f"Domain:   {tech}\n"
                            f"Assignee: {assignee}\n"
                            f"Lapse:    {lapse}\n"
                            f"Score:    {score}/99\n\n"
                            f"COMMERCIAL OPPORTUNITY\n{'-'*30}\n{pitch}\n\n"
                            f"TECHNICAL ABSTRACT\n{'-'*30}\n{abstract_text}\n\n"
                            f"Generated by PatentMine"
                        )
                        st.download_button(
                            "⬇ Export Strategy Brief (.txt)",
                            data=blueprint,
                            file_name=f"PatentMine_{item['id']}_Brief.txt",
                            key=f"dl_{item['id']}",
                            use_container_width=True
                        )
                    with act2:
                        email = st.text_input(
                            "Alert Email",
                            key=f"email_{item['id']}",
                            placeholder="your@company.com",
                            label_visibility="collapsed"
                        )
                        if st.button("Add to Watchlist", key=f"watch_{item['id']}", use_container_width=True):
                            if email:
                                try:
                                    w = requests.post(
                                        "http://localhost:8000/watchlist",
                                        json={"patent_id": item['id'], "email": email}
                                    )
                                    if w.status_code == 200:
                                        st.success("Added to watchlist.")
                                except:
                                    st.error("Could not reach watchlist API.")
                            else:
                                st.warning("Enter an email address first.")


# ════════════════════════════════════════════════════════════
# TAB 2 — METRICS
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Live Database Metrics")
    try:
        stats_res = requests.get("http://localhost:8000/stats", timeout=5)
        if stats_res.status_code == 200:
            stats = stats_res.json()
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Patents Indexed", f"{stats.get('total_patents', 0):,}")
            c2.metric("Technology Domains", len(stats.get('domains', {})))
            c3.metric("API Status", "Online")

            domains_data = stats.get('domains', {})
            if domains_data:
                st.markdown("#### Patent Volume by Technology Domain")
                chart_df = pd.DataFrame(
                    list(domains_data.items()),
                    columns=["Domain", "Volume"]
                ).set_index("Domain")
                st.bar_chart(chart_df, color="#1e3a5f")
        else:
            st.warning("Backend returned an unexpected response.")
    except Exception as e:
        st.warning(f"Could not load metrics: backend may be offline.")
