from io import BytesIO
import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from github_client import calculate_community_health

# --- Layout Configuration ---
st.set_page_config(
    page_title="ScanAPI Community Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚀 ScanAPI Community Dashboard")
st.markdown("Monitor ecosystem contributions and project metrics.")
st.divider()

# --- Fetch Data Once ---
metrics = calculate_community_health("scanapi/scanapi")
df_issues = metrics["issues_df"]
df_pulls = metrics["pulls_df"]

# ---------------------------------------------------------
# 🏷️ DYNAMIC TAG DISCOVERY
# ---------------------------------------------------------
if not df_issues.empty and "labels" in df_issues.columns:
    all_extracted_labels = [
        label for sublist in df_issues["labels"] for label in sublist
    ]
    unique_labels = sorted(list(set(all_extracted_labels)))
else:
    unique_labels = []

# ---------------------------------------------------------
# 🎛️ SIDEBAR CONTROLS & FILTERING
# ---------------------------------------------------------
st.sidebar.header("🎯 Onboarding Filters")
st.sidebar.markdown("Narrow down beginner-friendly opportunities.")

difficulty_options = ["All Issues"]
for target_tag in ["good first issue", "help wanted"]:
    if target_tag in unique_labels:
        difficulty_options.append(target_tag)

beginner_filter = st.sidebar.radio(
    "Select Target Label:",
    options=difficulty_options,
    index=1 if len(difficulty_options) > 1 else 0,
)

technical_scope = st.sidebar.multiselect(
    "Filter by Technical Scope:",
    options=unique_labels,
    default=[],
    help="Select labels to match your skillset.",
)

if not df_issues.empty:
    filtered_df = df_issues.copy()

    # Apply Difficulty Filter
    if beginner_filter != "All Issues":
        filtered_df = filtered_df[
            filtered_df["labels"].apply(
                lambda tg: any(
                    beginner_filter.lower() == t.lower() for t in tg
                )
            )
        ]

    # Apply Technical Scope Filter
    if technical_scope:
        selected_scopes = [s.lower() for s in technical_scope]
        filtered_df = filtered_df[
            filtered_df["labels"].apply(
                lambda tg: any(
                    s in [t.lower() for t in tg] for s in selected_scopes
                )
            )
        ]
else:
    filtered_df = pd.DataFrame()

# --- Tab Layout ---
tab_onb, tab_lead, tab_trend, tab_market = st.tabs(
    ["📥 Onboarding Portal", "🏆 Leaderboard", "📈 Trends", "📱 Marketing"]
)

# ---------------------------------------------------------
# 📥 TAB 1: CONTRIBUTOR ONBOARDING HUB
# ---------------------------------------------------------
with tab_onb:
    st.header("Contributor Onboarding Hub")
    st.subheader("Lowering the barrier to entry")

    st.markdown("### 📊 Project Health & Responsiveness")
    col1, col2 = st.columns(2)

    with col1:
        ttfr = metrics["avg_ttfr_hours"]
        st.metric(
            label="⏱️ Avg Time-to-First-Response (TTFR)",
            value=f"{ttfr:.2f} hrs" if pd.notna(ttfr) else "N/A",
            # delta="Target: < 24h",
        )
    with col2:
        ttm = metrics["avg_ttm_hours"]
        st.metric(
            label="🚀 Avg Time-to-Merge (TTM)",
            value=f"{ttm:.2f} hrs" if pd.notna(ttm) else "N/A",
            # delta="Target: < 48h",
        )

    st.divider()

    st.markdown(f"### 🎯 Open Opportunities: `{beginner_filter}`")
    st.write(
        "Find outstanding tasks tailored for your skillset. "
        "Use the left sidebar to fine-tune lists."
    )

    if not filtered_df.empty:
        display_df = filtered_df[
            ["number", "title", "labels", "assignee", "created_at"]
        ]
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info(
            "✨ No active open issues match your filters. "
            "Try broadening your sidebar selections!"
        )

# ---------------------------------------------------------
# 🏆 TAB 2: LEADERBOARD
# ---------------------------------------------------------
with tab_lead:
    st.header("Wall of Fame")
    if not df_pulls.empty:
        st.dataframe(df_pulls, use_container_width=True)

# ---------------------------------------------------------
# 📈 TAB 3: TRENDS
# ---------------------------------------------------------
with tab_trend:
    st.header("Issue Trend Analysis")

# ---------------------------------------------------------
# 📱 TAB 4: MARKETING & SOCIAL MEDIA ASSETS
# ---------------------------------------------------------
with tab_market:
    st.header("Social Media Assets & Advocacy Hub")
    st.subheader("Amplify community wins instantly")

    st.markdown("### 📝 Weekly Progress Snippet")
    st.write("Copy this data-driven summary to share your project momentum.")

    if not df_pulls.empty:
        total_prs = len(df_pulls)
        has_asg = "assignee" in df_pulls.columns
        unique_authors = df_pulls["assignee"].nunique() if has_asg else 1
        if unique_authors == 0:
            unique_authors = 1
    else:
        total_prs = 0
        unique_authors = 0

    marketing_text = (
        f"🔥 Huge shoutout to the ScanAPI ecosystem!\n\n"
        f"This week, our community successfully merged {total_prs} "
        f"Pull Requests driven by {unique_authors} unique authors! 🚀"
        f"\n\nCheck out our performance metrics and contribute: "
        f"https://github.com ✨"
    )

    st.text_area(
        label="Generated Social Post Summary:",
        value=marketing_text,
        height=180,
        help="Click the copy icon in the upper right corner to copy.",
    )

    st.divider()

    st.markdown("### 🎨 Dynamic Contributor Card Generator")
    st.write(
        "Generate custom-branded milestone graphics to celebrate "
        "outstanding contributors."
    )

    c_handle = st.text_input(
        "Enter Contributor GitHub Username:", "developer_name"
    )
    milestone_text = st.text_input(
        "Enter Achievement Milestone:", "Core optimization!"
    )

    if st.button("Generate Branded Milestone Card"):
        card_w, card_h = 800, 400
        scanapi_dark = (15, 23, 42)
        scanapi_electric = (56, 189, 248)
        white = (255, 255, 255)

        img = Image.new("RGB", (card_w, card_h), color=scanapi_dark)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (card_w, 15)], fill=scanapi_electric)

        font_title = ImageFont.load_default()

        draw.text(
            (50, 60), "ScanAPI Community Milestone", fill=scanapi_electric
        )
        draw.text((50, 120), f"🎉 Congratulations, @{c_handle}!", fill=white)
        draw.text((50, 180), f"Contribution: {milestone_text}", fill=white)
        draw.text(
            (50, 330),
            "Powered by ScanAPI Dashboard 🚀",
            fill=(100, 116, 139),
        )

        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(
            img, caption="Preview Generated Card", use_container_width=True
        )

        st.download_button(
            label="📥 Download Milestone Card (.png)",
            data=byte_im,
            file_name=f"scanapi_milestone_{c_handle}.png",
            mime="image/png",
        )

st.sidebar.markdown("---")
st.sidebar.markdown("💡 [ScanAPI Repo](https://github.com)")
