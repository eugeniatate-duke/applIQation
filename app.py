import streamlit as st
from pathlib import Path

from src.llm_assessor import assess_candidate

st.set_page_config(
    page_title="ApplIQation",
    page_icon="🎯",
    layout="wide"
)

# ---------- Styling ----------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.big-score {
    font-size: 64px;
    font-weight: 700;
    text-align: center;
}

.score-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
}

.section-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.question-box {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------

st.title("🎯 ApplIQation")

st.caption(
    "AI-Powered Job Readiness Assessment"
)

st.markdown(
    """
Determine whether you're truly ready for a role by comparing your
resume against a target job description and generating assessment
questions that validate your preparedness.
"""
)

st.divider()

# ---------- Inputs ----------

left, right = st.columns(2)

with left:
    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["txt"]
    )

with right:
    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

analyze = st.button(
    "Analyze Readiness",
    use_container_width=True
)

# ---------- Results ----------

if analyze:

    if uploaded_resume is None:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description:
        st.error("Please paste a job description.")
        st.stop()

    resume_text = uploaded_resume.read().decode()

    with st.spinner(
        "Analyzing candidate readiness..."
    ):

        result = assess_candidate(
            resume_text,
            job_description
        )

    score = result["readiness_score"]

    st.divider()

    score_col, rec_col = st.columns([1, 2])

    with score_col:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="big-score">{score}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(score / 100)

    with rec_col:

        recommendation = result["recommendation"]

        if recommendation == "Ready Now":
            st.success(recommendation)

        elif recommendation == "Ready With Short Ramp-Up":
            st.warning(recommendation)

        else:
            st.error(recommendation)

    st.divider()

    col1, col2 = st.columns(2)

    # Strengths

    with col1:

        st.subheader("✅ Strengths")

        for item in result["strengths"]:
            st.success(item)

    # Gaps

    with col2:

        st.subheader("⚠️ Competency Gaps")

        for item in result["gaps"]:
            st.warning(item)

    st.divider()

    st.subheader("🧠 Readiness Validation Questions")

    for i, question in enumerate(
        result["assessment_questions"],
        start=1
    ):
        with st.expander(
            f"Question {i}"
        ):
            st.write(question)