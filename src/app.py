import streamlit as st

# Initial page configuration
st.set_page_config(
    page_title="ScanAPI Community Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main Dashboard Title
st.title("🚀 ScanAPI Community Dashboard")
st.markdown(
    "Welcome to the community health and velocity dashboard. "
    "This tool monitors ecosystem contributions, project metrics, "
    "and generates social assets."
)

st.divider()

# Navigation Tabs Creation (Mapping the next project features)
tab_onboarding, tab_leaderboard, tab_trends, tab_marketing = st.tabs(
    [
        "📥 Contributor Onboarding",
        "🏆 Wall of Fame & Leaderboard",
        "📈 Issue Trend Analytics",
        "📱 Social Media Assets",
    ]
)

# TAB CONTENT (Initial boilerplates)

with tab_onboarding:
    st.header("Contributor Onboarding Hub")
    st.subheader("Lowering the barrier to entry")
    st.info(
        "Feature incoming: Dynamic aggregation of "
        "'good first issue' and 'help wanted' labels."
    )

    # Visual example of metric cards (TTFR and TTM)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Avg Time-to-First-Response (TTFR)",
            value="⏳ Loading...",
            delta="Target: < 24h",
        )
    with col2:
        st.metric(
            label="Avg Time-to-Merge (TTM)",
            value="⏳ Loading...",
            delta="Target: < 48h",
        )

with tab_leaderboard:
    st.header("Community Wall of Fame")
    st.subheader("Celebrating our active contributors")
    st.info(
        "Feature incoming: Interactive leaderboard ranking "
        "active contributors and PR authors."
    )

with tab_trends:
    st.header("Advanced Issue Trend Analysis")
    st.subheader("Project resolution velocity over time")
    st.info(
        "Feature incoming: Interactive time-series charts "
        "tracking issue activity grouped by labels."
    )

with tab_marketing:
    st.header("Social Media Helper & Automation")
    st.subheader("Empowering community advocates")
    st.info(
        "Feature incoming: Automated text templates and dynamic "
        "'Contributor of the Week' image generators."
    )

# Minimalist Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **ScanAPI Ecosystem**")
st.sidebar.markdown("[Main Repository](https://github.com/scanapi/scanapi)")
