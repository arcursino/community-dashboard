import streamlit as st
import pandas as pd  # Added to handle missing or null metric values (pd.notna)
from github_client import (
    calculate_community_health,
)  # Added to access your metric module
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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

# ---------------------------------------------------------
# 📱 TAB 4: MARKETING & SOCIAL MEDIA ASSETS
# ---------------------------------------------------------
with tab_marketing:
    st.header("Social Media Assets & Advocacy Hub")
    st.subheader("Amplify community wins instantly")

    st.markdown("### 📝 Weekly Progress Snippet")
    st.write(
        "Copy this data-driven summary to share your project momentum on Twitter/X, LinkedIn, or Discord."
    )

    # Calculate metrics for the text template from df_pulls
    if not df_pulls.empty:
        total_prs = len(df_pulls)
        # Assuming the author's login profile name is nested or tracked under 'assignee' or similar profile identifier
        # If your pull dataframe records an 'author' column from earlier parsing, use that. Fallback to unique titles/assignees if needed.
        unique_authors = (
            df_pulls["assignee"].nunique() if "assignee" in df_pulls.columns else 1
        )
        if unique_authors == 0:
            unique_authors = 1
    else:
        total_prs = 0
        unique_authors = 0

    # Build the dynamic f-string template
    marketing_text = (
        f"🔥 Huge shoutout to the ScanAPI ecosystem!\n\n"
        f"This week, our incredible community successfully closed and merged {total_prs} Pull Requests "
        f"driven by {unique_authors} unique open-source authors! 🚀\n\n"
        f"Check out our performance metrics and see how you can make your first contribution here: "
        f"https://github.com/scanapi/scanapi"
    )
    st.text_area(
        label="Generated Social Post Summary:",
        value=marketing_text,
        height=180,
        help="Click the copy icon in the upper right corner of this box to copy the text.",
    )

    st.divider()

    st.markdown("### 🎨 Dynamic Contributor Card Generator")
    st.write(
        "Generate custom-branded milestone graphics to celebrate outstanding contributors."
    )

    # Inputs for customization
    contributor_handle = st.text_input(
        "Enter Contributor GitHub Username:", "developer_name"
    )
    milestone_text = st.text_input(
        "Enter Achievement Milestone:", "Merged a major core logic optimization!"
    )

    if st.button("Generate Branded Milestone Card"):
        # 1. Create a base canvas with ScanAPI brand colors (Dark background)
        card_width = 800
        card_height = 400
        scanapi_dark_blue = (15, 23, 42)  # RGB matching modern dark UI
        scanapi_electric_blue = (56, 189, 248)  # RGB accent cyan
        white = (255, 255, 255)

        img = Image.new("RGB", (card_width, card_height), color=scanapi_dark_blue)
        draw = ImageDraw.Draw(img)

        # 2. Draw branded border/accent line at the top boundary
        draw.rectangle([(0, 0), (card_width, 15)], fill=scanapi_electric_blue)

        # 3. Load basic default fonts (Safe fallback across environments without external .ttf assets)
        try:
            # Try loading a default system font if available, else fallback
            font_title = ImageFont.load_default()
        except Exception:
            font_title = ImageFont.load_default()

        # 4. Burn textual data onto the background image surface
        # Using simple pixel-positioned draws to safely output details
        draw.text((50, 60), "ScanAPI Community Milestone", fill=scanapi_electric_blue)
        draw.text((50, 120), f"🎉 Congratulations, @{contributor_handle}!", fill=white)
        draw.text((50, 180), f"Contribution: {milestone_text}", fill=white)
        draw.text(
            (50, 330),
            "Powered by ScanAPI Dashboard 🚀",
            fill=(100, 116, 139),
        )

        # 5. Convert Image object into bytes for Streamlit downloader interface
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display image preview in Streamlit canvas
        st.image(img, caption="Preview Generated Card", use_container_width=True)

        # Download interface trigger button
        st.download_button(
            label="📥 Download Milestone Card (.png)",
            data=byte_im,
            file_name=f"scanapi_milestone_{contributor_handle}.png",
            mime="image/png",
        )

# Minimalist Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **ScanAPI Ecosystem**")
st.sidebar.markdown("[Main Repository](https://github.com/scanapi/scanapi)")
