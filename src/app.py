import streamlit as st
import pandas as pd  # Added to handle missing or null metric values (pd.notna)
from github_client import (
    calculate_community_health,
)  # Added to access your metric module


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

# --- Fetch Data Once ---
metrics = calculate_community_health("scanapi/scanapi")
df_issues = metrics["issues_df"]
df_pulls = metrics["pulls_df"]

# ---------------------------------------------------------
# 🎛️ SIDEBAR CONTROLS & FILTERING (Issue #2 Focus)
# ---------------------------------------------------------
st.sidebar.header("🎯 Onboarding Filters")
st.sidebar.markdown("Narrow down beginner-friendly opportunities.")

# 1. Filter by Difficulty Label
beginner_filter = st.sidebar.radio(
    "Select Target Label:",
    options=["All Issues", "good first issue", "help wanted"],
    index=1,  # Defaults to 'good first issue' to lower the barrier immediately
)

# 2. Filter by Technical Scope
technical_scope = st.sidebar.multiselect(
    "Filter by Technical Scope:",
    options=["documentation", "tests", "bug", "feature", "refactor"],
    default=[],
    help="Select one or more labels to match your technical skillset.",
)

# --- Apply Sidebar Filters to Dataframe ---
if not df_issues.empty:
    filtered_df = df_issues.copy()

    # Apply Difficulty Filter
    if beginner_filter != "All Issues":
        # Convert tags to lowercase for a reliable match
        filtered_df = filtered_df[
            filtered_df["labels"].apply(
                lambda tags: any(beginner_filter.lower() == t.lower() for t in tags)
            )
        ]

    # Apply Technical Scope Filter
    if technical_scope:
        # Convert selected filter criteria to lowercase
        selected_scopes = [s.lower() for s in technical_scope]

        # Match if ANY of the lowercase selected filters exist in the lowercase issue tags
        filtered_df = filtered_df[
            filtered_df["labels"].apply(
                lambda tags: any(
                    s in [t.lower() for t in tags] for s in selected_scopes
                )
            )
        ]
else:
    filtered_df = pd.DataFrame()

# Navigation Tabs Creation (Mapping the next project features)
tab_onboarding, tab_leaderboard, tab_trends, tab_marketing = st.tabs(
    [
        "📥 Contributor Onboarding",
        "🏆 Wall of Fame & Leaderboard",
        "📈 Issue Trend Analytics",
        "📱 Social Media Assets",
    ]
)

# TAB CONTENT

with tab_onboarding:
    st.header("Contributor Onboarding Hub")
    st.subheader("Lowering the barrier to entry")

    # Section 1: Performance Transparency Panel
    st.markdown("### 📊 Project Health & Responsiveness")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="⏱️ Avg Time-to-First-Response (TTFR)",
            value=(
                f"{metrics['avg_ttfr_hours']:.2f} hrs"
                if pd.notna(metrics["avg_ttfr_hours"])
                else "N/A"
            ),
            # delta="Target: < 24h",
        )
    with col2:
        st.metric(
            label="🚀 Avg Time-to-Merge (TTM)",
            value=(
                f"{metrics['avg_ttm_hours']:.2f} hrs"
                if pd.notna(metrics["avg_ttm_hours"])
                else "N/A"
            ),
            # delta="Target: < 48h",
        )

    st.divider()

    # Section 2: Dynamic Beginner Issue Board
    st.markdown(f"### 🎯 Open Opportunities: `{beginner_filter}`")
    st.write(
        "Find outstanding tasks tailored for your skillset. Use the left sidebar to fine-tune lists."
    )

    if not filtered_df.empty:
        # Streamline display by dropping raw IDs and cleaning layout columns
        display_df = filtered_df[
            ["number", "title", "labels", "assignee", "created_at"]
        ]
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info(
            "✨ No active open issues match your specific combination of filters. Try broadening your sidebar selections!"
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
