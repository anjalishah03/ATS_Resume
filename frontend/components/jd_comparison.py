
from typing import Any, Dict, Optional

import streamlit as st


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return  # caller decides whether to render the section at all

    st.markdown(
        """
        <style>
        .jd-section-subtitle {
            color: #64748B;
            font-size: 14px;
            margin-top: -8px;
            margin-bottom: 22px;
        }

        .jd-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }

        .jd-card-title {
            color: #1E293B;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .jd-keyword {
            display: inline-block;
            background: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
            border-radius: 8px;
            padding: 6px 10px;
            margin: 4px 4px 4px 0;
            font-size: 13px;
            font-weight: 600;
        }

        .jd-missing-keyword {
            display: inline-block;
            background: #FFF1F2;
            color: #BE123C;
            border: 1px solid #FECDD3;
            border-radius: 8px;
            padding: 6px 10px;
            margin: 4px 4px 4px 0;
            font-size: 13px;
            font-weight: 600;
        }

        .jd-gap-skill {
            display: inline-block;
            background: #FFF7ED;
            color: #C2410C;
            border: 1px solid #FED7AA;
            border-radius: 8px;
            padding: 6px 10px;
            margin: 4px 4px 4px 0;
            font-size: 13px;
            font-weight: 600;
        }

        .jd-empty-state {
            color: #64748B;
            font-size: 14px;
            padding: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 Job Description Match")
    st.markdown(
        '<p class="jd-section-subtitle">'
        'Compare your resume against the job requirements.'
        '</p>',
        unsafe_allow_html=True,
    )

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic = float(jd_comparison.get("semantic_similarity", 0))
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []
    gap = jd_comparison.get("skills_gap", []) or []

    top_l, top_r = st.columns(2, gap="medium")

    with top_l:
        st.markdown(
            '<div class="jd-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jd-card-title">🎯 Match Percentage</div>',
            unsafe_allow_html=True,
        )
        st.metric("Match Percentage", f"{match_pct:.0f}%")
        st.progress(min(max(match_pct / 100.0, 0.0), 1.0))

        st.markdown(
            '<div class="jd-card-title" style="margin-top:22px;">'
            '🧠 Semantic Similarity</div>',
            unsafe_allow_html=True,
        )
        st.metric("Semantic Similarity", f"{semantic * 100:.0f}%")
        st.progress(min(max(semantic, 0.0), 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    with top_r:
        st.markdown(
            '<div class="jd-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jd-card-title">✅ Matched Keywords</div>',
            unsafe_allow_html=True,
        )

        if matched:
            st.markdown(
                "".join(
                    f'<span class="jd-keyword">{kw}</span>'
                    for kw in matched[:15]
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="jd-empty-state">None matched yet</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    bot_l, bot_r = st.columns(2, gap="medium")

    with bot_l:
        st.markdown(
            '<div class="jd-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jd-card-title">❌ Missing Keywords</div>',
            unsafe_allow_html=True,
        )

        if missing:
            st.markdown(
                "".join(
                    f'<span class="jd-missing-keyword">{kw}</span>'
                    for kw in missing[:10]
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="jd-empty-state">'
                'All key terms are present!</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with bot_r:
        st.markdown(
            '<div class="jd-card">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="jd-card-title">📊 Skills Gap</div>',
            unsafe_allow_html=True,
        )

        if gap:
            st.markdown(
                "".join(
                    f'<span class="jd-gap-skill">{skill}</span>'
                    for skill in gap[:10]
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="jd-empty-state">'
                'No significant skills gap detected</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
