import streamlit as st
import pandas as pd  # Added to handle missing or null metric values (pd.notna)
from github_client import (
    calculate_community_health,
)  # Added to access your metric module

# Automatically pull metrics for the main ScanAPI repository
metrics = calculate_community_health("scanapi/scanapi")

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

    # Visual metrics extracted dynamically from the GitHub client module
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Avg Time-to-First-Response (TTFR)",
            value=(
                f"{metrics['avg_ttfr_hours']:.2f} hrs"
                if pd.notna(metrics["avg_ttfr_hours"])
                else "N/A"
            ),
            # delta="Target: < 24h",
        )
    with col2:
        st.metric(
            label="Avg Time-to-Merge (TTM)",
            value=(
                f"{metrics['avg_ttm_hours']:.2f} hrs"
                if pd.notna(metrics["avg_ttm_hours"])
                else "N/A"
            ),
            # delta="Target: < 48h",
        )

    # Render raw issues dataframe beneath metrics if data exists
    if not metrics["issues_df"].empty:
        st.subheader("📋 Active Issue Stream")
        st.dataframe(metrics["issues_df"], use_container_width=True)


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
