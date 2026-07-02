import pandas as pd
from github import Github, RateLimitExceededException
import streamlit as st


def get_github_client():
    """
    Fetches the token from secrets.toml and initializes
    the GitHub client. Streamlit automatically searches
    within .streamlit/secrets.toml.
    """
    token = st.secrets.get("GITHUB_TOKEN", None)
    if token:
        return Github(token)
    # Fallback to unauthenticated client (lower rate limits)
    return Github()


@st.cache_data(ttl=900, show_spinner="Fetching GitHub community metrics...")
def fetch_raw_repo_data(repo_name: str):
    """
    Fetches raw issues and pull requests data from the
    specified repository. Caches data for 15 minutes.
    """
    g = get_github_client()

    try:
        repo = g.get_repo(repo_name)
        issues_data = []
        pulls_data = []

        # Limiting to the 100 most recent items
        for issue in repo.get_issues(state="all")[:100]:
            base_info = {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "created_at": issue.created_at,
                "closed_at": issue.closed_at,
                "labels": [label.name for label in issue.labels],
                "assignee": (issue.assignee.login if issue.assignee else None),
                # Add these two new keys to track the real author details:
                "author": (issue.user.login if issue.user else "Unknown"),
                "avatar_url": (
                    issue.user.avatar_url
                    if issue.user
                    else "https://github.com"
                ),
            }

            if issue.pull_request:
                # Process item as a Pull Request
                pr = repo.get_pull(issue.number)
                base_info["merged_at"] = pr.merged_at
                base_info["is_merged"] = pr.merged
                pulls_data.append(base_info)
            else:
                # Process item as a standard Issue
                comments = issue.get_comments()
                if comments.totalCount > 0:
                    first_comment_time = comments[0].created_at
                else:
                    first_comment_time = None
                base_info["first_response_at"] = first_comment_time
                issues_data.append(base_info)

        return {"issues": issues_data, "pulls": pulls_data}

    except RateLimitExceededException:
        st.error("💥 GitHub API Rate limit reached!")
        return {"issues": [], "pulls": []}


def calculate_community_health(repo_name: str):
    """
    Transforms raw dictionary arrays into structured DataFrames.
    Calculates key performance metrics: TTFR and TTM.
    """
    raw_data = fetch_raw_repo_data(repo_name)

    df_issues = pd.DataFrame(raw_data["issues"])
    df_pulls = pd.DataFrame(raw_data["pulls"])

    # --- Time-to-First-Response (TTFR) Calculation ---
    if not df_issues.empty:
        df_issues["created_at"] = pd.to_datetime(df_issues["created_at"])
        df_issues["first_response_at"] = pd.to_datetime(
            df_issues["first_response_at"]
        )
        time_diff = df_issues["first_response_at"] - df_issues["created_at"]
        df_issues["ttfr_hours"] = time_diff.dt.total_seconds() / 3600
        avg_ttfr = df_issues["ttfr_hours"].mean()
    else:
        avg_ttfr = None

    # --- Time-to-Merge (TTM) Calculation ---
    if not df_pulls.empty:
        df_pulls["created_at"] = pd.to_datetime(df_pulls["created_at"])
        df_pulls["merged_at"] = pd.to_datetime(df_pulls["merged_at"])
        # E712 fix: checking boolean directly without '== True'
        merged_prs = df_pulls[df_pulls["is_merged"]].copy()
        time_diff_pr = merged_prs["merged_at"] - merged_prs["created_at"]
        merged_prs["ttm_hours"] = time_diff_pr.dt.total_seconds() / 3600
        avg_ttm = merged_prs["ttm_hours"].mean()
    else:
        avg_ttm = None

    return {
        "issues_df": df_issues,
        "pulls_df": df_pulls,
        "avg_ttfr_hours": avg_ttfr,
        "avg_ttm_hours": avg_ttm,
    }
