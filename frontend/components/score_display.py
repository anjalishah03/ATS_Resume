from typing import Any, Dict

import streamlit as st

from frontend.components._helpers import get_score_color, get_score_emoji


# Component max scores match backend/core/config.py SCORE_WEIGHTS.
# (Backend returns each component's score on its own scale, not 0–100.)
COMPONENTS = [
    ("Formatting",        "formatting",        20, "📝"),
    ("Keywords & Skills", "keywords",          25, "🔑"),
    ("Content Quality",   "content",           25, "📄"),
    ("Skill Validation",  "skill_validation",  15, "✅"),
    ("ATS Compatibility", "ats_compatibility", 15, "🤖"),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    """Big colored score card with a short interpretation line."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    text_color, bg_color = get_score_color(score)
    emoji = get_score_emoji(score)

    st.markdown(
        """
        <style>
        .ats-score-card {
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            padding: 32px 24px;
            text-align: center;
            box-shadow: 0 12px 30px rgba(49,46,129,0.16);
            background: linear-gradient(
                135deg, #312E81 0%, #4338CA 55%, #6366F1 100%
            );
        }
        .ats-score-label {
            color: #E0E7FF;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }
        .ats-score-value {
            color: #FFFFFF;
            font-size: 68px;
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -2px;
            margin: 8px 0;
        }
        .ats-score-title {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 650;
            margin: 10px 0;
        }
        .ats-score-interpretation {
            color: #E0E7FF;
            font-size: 15px;
            line-height: 1.7;
            margin: 12px auto 0;
            max-width: 500px;
        }
        @media (max-width: 640px) {
            .ats-score-card {
                padding: 24px 16px;
                border-radius: 16px;
            }
            .ats-score-value {
                font-size: 52px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    st.markdown("## 📊 Analysis Results")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            f"""
            <div class="ats-score-card">
                <div class="ats-score-label">Resume Analysis</div>
                <div class="ats-score-value">
                    {emoji} {score:.0f}
                </div>
                <div class="ats-score-title">Overall ATS Score</div>
                <div style="
                    display:inline-block;
                    background:{bg_color};
                    color:{text_color};
                    padding:6px 16px;
                    border-radius:999px;
                    font-size:13px;
                    font-weight:700;
                    margin-top:8px;
                ">
                    Score Overview
                </div>
                <div class="ats-score-interpretation">
                    {interpretation}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )



def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    """Five progress bars, one per scoring component."""
    component_scores = analysis.get("component_scores") or {}
    st.markdown("### 📈 Score Breakdown")

    left, right = st.columns(2)
    for i, (label, key, max_score, icon) in enumerate(COMPONENTS):
        value = float(component_scores.get(key, 0))
        percentage = value / max_score if max_score else 0
        bar_color = "green" if percentage >= 0.8 else "orange" if percentage >= 0.6 else "red"

        with left if i % 2 == 0 else right:
            st.markdown(f"**{icon} {label}**")
            st.markdown(
                f"""
                <div style="background-color:#e0e0e0; border-radius:10px; height:20px; margin-bottom:5px;">
                    <div style="background-color:{bar_color}; width:{percentage * 100}%;
                                height:100%; border-radius:10px; transition:width 0.5s;"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"**{value:.0f}/{max_score}**")
            st.markdown("")
