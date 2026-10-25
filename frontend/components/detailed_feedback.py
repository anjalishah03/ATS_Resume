
from typing import Any, Dict, List

import streamlit as st

from frontend.components._helpers import get_severity_style


SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        level = (issue.get("severity_level") or "low").lower()
        grouped.setdefault(level, []).append(issue)
    return grouped


def _render_issue(issue: Dict[str, Any]) -> None:
    icon, text_color, bg_color = get_severity_style(
        issue.get("severity_level") or "low"
    )
    title = issue.get("issue_title", "Untitled issue")
    impact = issue.get("ats_impact", "")
    explanation = issue.get("explanation", "")
    where = issue.get("where_it_appears", "")
    how_to_fix = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example = issue.get("example_improvement", "")

    st.markdown(
        """
        <style>
        .feedback-issue-card {
            border-radius: 14px;
            padding: 16px 18px;
            margin: 10px 0 14px 0;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            border: 1px solid #E2E8F0;
        }

        .feedback-issue-title {
            font-size: 16px;
            font-weight: 700;
            line-height: 1.5;
        }

        .feedback-issue-impact {
            font-size: 13px;
            font-weight: 500;
            margin-top: 6px;
            opacity: 0.9;
        }

        .feedback-section-heading {
            color: #1E293B;
            font-weight: 750;
            margin-top: 24px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #E2E8F0;
        }

        .feedback-details-label {
            color: #334155;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="feedback-issue-card"
             style="border-left:5px solid {text_color};
                    background:{bg_color};">
            <div class="feedback-issue-title" style="color:{text_color};">
                {icon} {title}
            </div>
            <div class="feedback-issue-impact" style="color:{text_color};">
                {impact}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📋 View Details & Recommendations", expanded=False):
        if explanation:
            st.markdown(
                f'<span class="feedback-details-label">🔎 What\'s happening</span>',
                unsafe_allow_html=True,
            )
            st.markdown(explanation)

        if where:
            st.markdown(
                '<span class="feedback-details-label">📍 Where it appears</span>',
                unsafe_allow_html=True,
            )
            st.markdown(where)

        if how_to_fix:
            st.markdown(
                '<span class="feedback-details-label">🛠️ How to fix</span>',
                unsafe_allow_html=True,
            )
            st.markdown(how_to_fix)

        if action_items:
            st.markdown(
                '<span class="feedback-details-label">✅ Action items</span>',
                unsafe_allow_html=True,
            )
            for item in action_items:
                st.markdown(f"- {item}")

        if example:
            st.markdown(
                '<span class="feedback-details-label">✨ Example improvement</span>',
                unsafe_allow_html=True,
            )
            st.code(example, language="text")


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return  # backend produced no per-issue feedback this run

    st.markdown("### 🔍 Detailed Feedback")
    st.caption(f"{len(issues)} issue(s) flagged — grouped by severity.")

    grouped = _group_by_severity(issues)
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        st.markdown(
            f'<div class="feedback-section-heading">'
            f'{level.title()} ({len(items)})</div>',
            unsafe_allow_html=True,
        )
        for issue in items:
            _render_issue(issue)
